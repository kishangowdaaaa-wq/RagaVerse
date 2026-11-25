
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector

from app.database.base import Base


class KnowledgeEmbedding(Base):
    """Stores Carnatic music knowledge and its vector embedding."""

    __tablename__ = "knowledge_embeddings"

    __table_args__ = (
        UniqueConstraint(
            "source_type",
            "source_id",
            name="uq_knowledge_source",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    content = Column(
        Text,
        nullable=False,
    )

    source_type = Column(
        String(50),
        nullable=False,
        index=True,
    )

    source_id = Column(
        String(150),
        nullable=False,
    )

    embedding = Column(
        Vector(768),
        nullable=False,
    )

    metadata_json = Column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
