from sqlalchemy import Column, Integer, String, DateTime, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from core.database import Base

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    vector_id = Column(String, nullable=False, unique=True)  # Qdrant vector ID
    chunk_strategy = Column(String, nullable=False)
    additional_metadata = Column(JSONB, nullable=True)  # e.g., author, tags
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class InterviewBooking(Base):
    __tablename__ = "interview_booking"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, index=True)
    interview_date = Column(DateTime, nullable=False)
    time_slot = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
