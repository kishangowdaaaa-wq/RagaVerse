
from functools import lru_cache

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized and validated application configuration."""

    app_name: str = "RagaVerse"
    app_version: str = "0.1.0"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    # Database
    db_user: str = "postgres"
    db_password: SecretStr
    db_host: str = "localhost"
    db_port: int = Field(default=5432, ge=1, le=65535)
    db_name: str = "ragaverse_db"

    # Authentication
    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = Field(
        default=30,
        ge=1,
        le=1440,
    )

    # OpenAI configuration
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-5.5"

    # Embedding configuration
    embedding_provider: str = "ollama"
    embedding_model: str = "nomic-embed-text"
    embedding_dimensions: int = Field(
        default=768,
        ge=256,
        le=3072,
    )
    ollama_base_url: str = "http://localhost:11434"

    # CORS configuration
    cors_origins: list[str] = Field(
        default=[
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    # Conversation management
    conversation_history_limit: int = Field(
        default=20,
        ge=2,
        le=100,
    )

    # LLM context management
    llm_max_input_tokens: int = Field(
        default=8000,
        ge=1000,
        le=100000,
    )
    llm_reserved_output_tokens: int = Field(
        default=1500,
        ge=100,
        le=16000,
    )

    # LLM reliability
    llm_timeout_seconds: float = Field(
        default=60.0,
        ge=5.0,
        le=300.0,
    )
    llm_max_retries: int = Field(
        default=2,
        ge=0,
        le=5,
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        value = value.strip().lower()

        if value not in {"development", "testing", "production"}:
            raise ValueError(
                "Environment must be development, testing, or production."
            )

        return value

    @field_validator("algorithm")
    @classmethod
    def validate_algorithm(cls, value: str) -> str:
        if value != "HS256":
            raise ValueError("Only HS256 is currently supported.")

        return value

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: SecretStr) -> SecretStr:
        secret = value.get_secret_value()

        if len(secret) < 32:
            raise ValueError(
                "SECRET_KEY must contain at least 32 characters."
            )

        return value

    @field_validator("db_user", "db_host", "db_name", "embedding_model")
    @classmethod
    def validate_nonempty_strings(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Configuration values cannot be empty.")

        return value

    @field_validator("ollama_base_url")
    @classmethod
    def validate_ollama_url(cls, value: str) -> str:
        value = value.strip().rstrip("/")

        if not value.startswith(("http://", "https://")):
            raise ValueError(
                "OLLAMA_BASE_URL must be an HTTP or HTTPS URL."
            )

        return value

    @field_validator("cors_origins")
    @classmethod
    def validate_cors_origins(cls, origins: list[str]) -> list[str]:
        cleaned = []

        for origin in origins:
            origin = origin.strip().rstrip("/")

            if not origin.startswith(("http://", "https://")):
                raise ValueError(
                    "CORS origins must use HTTP or HTTPS."
                )

            if origin == "*" or "*" in origin:
                raise ValueError(
                    "Wildcard CORS origins are not permitted."
                )

            cleaned.append(origin)

        return list(dict.fromkeys(cleaned))

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.environment == "production":
            if (
                "localhost" in self.ollama_base_url
                or "127.0.0.1" in self.ollama_base_url
            ):
                raise ValueError(
                    "Production Ollama URL must not use localhost."
                )

            if not self.cors_origins:
                raise ValueError(
                    "Production must configure at least one CORS origin."
                )

        return self

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
