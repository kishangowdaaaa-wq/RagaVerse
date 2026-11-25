
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from openai import OpenAIError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.config import get_settings
from app.database.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.prompts.carnatic import get_system_prompt
from app.schemas.conversation import (
    ChatResponse,
    ConversationCreate,
    ConversationDetailResponse,
    ConversationResponse,
    MessageCreate,
)
from app.services.llm import LLMService
from app.services.knowledge import get_rag_knowledge_context
from app.services.raga_comparison import (
    build_raga_comparison_context,
)
from app.services.intent_detection import detect_intent
from app.services.personalization import build_personalization_context
from app.services.token_manager import TokenManager

router = APIRouter()


INTENT_INSTRUCTIONS = {
    "raga_explanation": (
        "Explain the requested raga, including its arohanam, "
        "avarohanam, swaras, characteristics, and relevant details "
        "when supported by the retrieved knowledge."
    ),
    "raga_comparison": (
        "Compare the requested ragas systematically. Explain their "
        "arohanam, avarohanam, swara differences, and musical "
        "characteristics. Do not assume scale differences alone "
        "describe their complete identities."
    ),
    "tala_explanation": (
        "Explain the requested tala, including its structure, "
        "angas, beats, and practical rhythmic examples when supported "
        "by the available knowledge."
    ),
    "composition_information": (
        "Explain the requested composition, including its composer, "
        "raga, tala, language, and other available details. "
        "Do not invent missing information."
    ),
    "swaras_learning": (
        "Teach swaras systematically using beginner-friendly "
        "explanations and appropriate Carnatic notation."
    ),
    "general_carnatic": (
        "Answer the Carnatic music question clearly, using "
        "relevant terminology and examples."
    ),
    "out_of_scope": (
        "Politely explain that RagaVerse primarily specializes "
        "in Carnatic music and redirect the conversation when appropriate."
    ),
}


def get_owned_conversation(
    conversation_id: int,
    db: Session,
    current_user: User,
) -> Conversation:
    conversation = (
        db.query(Conversation)
        .filter(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
        )
        .first()
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return conversation


@router.post(
    "/",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Conversations"],
    summary="Create a new conversation",
)
def create_conversation(
    conversation_data: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationResponse:
    conversation = Conversation(
        title=conversation_data.title,
        user_id=current_user.id,
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    return conversation


@router.get(
    "/",
    response_model=list[ConversationResponse],
    tags=["Conversations"],
    summary="List the current user's conversations",
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[ConversationResponse]:
    return (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationDetailResponse,
    tags=["Conversations"],
    summary="Get a conversation with its messages",
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ConversationDetailResponse:
    return get_owned_conversation(
        conversation_id,
        db,
        current_user,
    )


@router.post(
    "/{conversation_id}/messages",
    response_model=ChatResponse,
    tags=["Conversations"],
    summary="Send a message to the RagaVerse AI assistant",
)
async def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    conversation = get_owned_conversation(
        conversation_id,
        db,
        current_user,
    )

    settings = get_settings()

    recent_messages = (
        db.query(Message)
        .filter(
            Message.conversation_id == conversation.id,
            Message.role.in_(["user", "assistant"]),
        )
        .order_by(
            Message.created_at.desc(),
            Message.id.desc(),
        )
        .limit(settings.conversation_history_limit)
        .all()
    )

    conversation_history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in reversed(recent_messages)
    ]

    conversation_history.append(
        {
            "role": "user",
            "content": message_data.content,
        }
    )

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=message_data.content,
    )

    db.add(user_message)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user_message)

    try:
        detected_intent = detect_intent(message_data.content)

        rag_context = await get_rag_knowledge_context(
            message_data.content,
            limit=5,
        )

        comparison_context = build_raga_comparison_context(
            message_data.content
        )

        # Load the current musician's saved profile.
        profile = current_user.profile

        preferred_level = (
            profile.preferred_learning_level
            if profile is not None
            else "beginner"
        )

        # Build the base prompt at the musician's preferred level.
        system_instructions = (
            get_system_prompt(preferred_level)
            + "\n\n"
            + "DETECTED QUESTION INTENT: "
            + detected_intent
            + "\n\n"
            + "INTENT-SPECIFIC GUIDANCE:\n"
            + INTENT_INSTRUCTIONS[detected_intent]
            + "\n\n"
            + rag_context
        )

        # Add saved musical preferences when a profile exists.
        personalization_context = build_personalization_context(
            profile
        )

        if personalization_context:
            system_instructions += (
                "\n\n"
                + personalization_context
            )

        if comparison_context:
            system_instructions += (
                "\n\n"
                + comparison_context
            )

        token_manager = TokenManager(
            model=settings.openai_model,
            max_input_tokens=settings.llm_max_input_tokens,
            reserved_output_tokens=settings.llm_reserved_output_tokens,
        )

        conversation_history = token_manager.trim_messages(
            conversation_history,
            instructions=system_instructions,
        )

        llm_service = LLMService()

        try:
            answer = await llm_service.generate_response(
                prompt=conversation_history,
                instructions=system_instructions,
            )
        finally:
            await llm_service.close()

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(exc),
        ) from exc

    except OpenAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=(
                "The AI service is temporarily unavailable. "
                "Your message was saved; please try again."
            ),
        ) from exc

    except Exception as exc:
        import logging

        logging.getLogger(__name__).exception(
            "RagaVerse AI generation failed."
        )

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Unable to generate an AI response. Please try again.",
        ) from exc

    assistant_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer,
    )

    db.add(assistant_message)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(assistant_message)

    return ChatResponse(
        user_message=user_message,
        assistant_message=assistant_message,
    )


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Conversations"],
    summary="Delete a conversation",
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    conversation = get_owned_conversation(
        conversation_id,
        db,
        current_user,
    )

    db.delete(conversation)
    db.commit()
