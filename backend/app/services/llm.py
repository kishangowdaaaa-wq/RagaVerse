
"""Local Ollama LLM service for the RagaVerse Carnatic music assistant."""

import logging
from typing import Any

import httpx

from app.core.config import get_settings


logger = logging.getLogger(__name__)


class LLMService:
    """Generate AI responses using a locally hosted Ollama model."""

    def __init__(self) -> None:
        settings = get_settings()

        self.model = "qwen2.5:3b"
        self.max_output_tokens = (
            settings.llm_reserved_output_tokens
        )

        self.client = httpx.AsyncClient(
            base_url=settings.ollama_base_url.rstrip("/"),
            timeout=settings.llm_timeout_seconds,
        )

    async def generate_response(
        self,
        prompt: str | list[dict[str, Any]],
        instructions: str | None = None,
    ) -> str:
        """Generate a response using the local Ollama API."""

        try:
            if isinstance(prompt, str):
                messages = [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            else:
                messages = [
                    {
                        "role": message["role"],
                        "content": message["content"],
                    }
                    for message in prompt
                ]

            if instructions:
                if messages and messages[0]["role"] == "system":
                    messages[0]["content"] = (
                        instructions
                        + "\n\n"
                        + messages[0]["content"]
                    )
                else:
                    messages.insert(
                        0,
                        {
                            "role": "system",
                            "content": instructions,
                        },
                    )

            response = await self.client.post(
                "/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "num_predict": self.max_output_tokens,
                    },
                },
            )

            response.raise_for_status()

            data = response.json()
            answer = data.get("message", {}).get("content", "")

            if not answer or not answer.strip():
                logger.warning(
                    "Ollama returned an empty response."
                )
                raise ValueError(
                    "The AI model returned an empty response."
                )

            return answer.strip()

        except ValueError:
            raise

        except Exception:
            logger.exception(
                "Local Ollama response generation failed."
            )
            raise

    async def close(self) -> None:
        """Close the asynchronous HTTP client."""

        await self.client.aclose()
