
"""Audio intelligence API endpoints for RagaVerse."""

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile,
)
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.deps import get_current_user
from app.models.user import User
from app.services.audio_intelligence import (
    AudioIntelligenceError,
    AudioIntelligenceService,
)
from app.services.audio_processing import AudioProcessingError
from app.services.pitch_detection import PitchDetectionError
from app.services.swara_identification import SwaraIdentificationError
from app.services.raga_detection import RagaDetectionError


router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

audio_service = AudioIntelligenceService()

MAX_FILE_SIZE_BYTES = (
    audio_service.audio_service.MAX_FILE_SIZE_BYTES
)


@router.post("/analyze")
@limiter.limit("5/minute")
async def analyze_audio(
    request: Request,
    file: UploadFile = File(...),
    tonic_frequency: float = Form(...),
    current_user: User = Depends(get_current_user),
):
    """Analyze an uploaded recording for an authenticated musician."""

    try:
        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="An audio filename is required.",
            )

        if tonic_frequency <= 0:
            raise HTTPException(
                status_code=422,
                detail="Tonic frequency must be positive.",
            )

        # Read one byte beyond the limit to detect oversized uploads.
        audio_bytes = await file.read(MAX_FILE_SIZE_BYTES + 1)

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="The uploaded audio file is empty.",
            )

        if len(audio_bytes) > MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=413,
                detail="Audio file exceeds the 20 MB size limit.",
            )

        result = await audio_service.analyze_audio(
            audio_bytes=audio_bytes,
            filename=file.filename,
            tonic_frequency=tonic_frequency,
        )

        return {
            "success": True,
            "message": "Audio analysis completed successfully.",
            "analysis": result,
        }

    except AudioIntelligenceError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except (
        AudioProcessingError,
        PitchDetectionError,
        SwaraIdentificationError,
        RagaDetectionError,
    ) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    finally:
        await file.close()
