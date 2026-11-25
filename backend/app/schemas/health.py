from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """
    Response schema for the application health endpoint.
    """

    status: str
    app_name: str
    version: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "status": "ok",
                "app_name": "RagaVerse",
                "version": "0.1.0",
            }
        }
    )