from sqlalchemy.orm import Session
from typing import List, Dict
from core import models

# ---------------- Document Metadata ----------------
def save_document_metadata(
    db: Session,
    file_name: str,
    chunks: List[str],
    vector_ids: List[str],
    chunk_strategy: str,
    additional_metadata: Dict = None
) -> None:
    for idx, (chunk, vec_id) in enumerate(zip(chunks, vector_ids)):
        db_obj = models.DocumentMetadata(
            file_name=file_name,
            chunk_text=chunk,
            chunk_index=idx,
            vector_id=vec_id,
            chunk_strategy=chunk_strategy,
            additional_metadata=additional_metadata or {}
        )
        db.add(db_obj)


def get_document_chunks(db: Session, file_name: str) -> List[models.DocumentMetadata]:
    return db.query(models.DocumentMetadata).filter_by(file_name=file_name).order_by(models.DocumentMetadata.chunk_index).all()


# ---------------- Interview Booking ----------------
def save_booking(
    db: Session,
    name: str,
    email: str,
    interview_date: str,
    time_slot: str,
    notes: str = None
) -> models.InterviewBooking:
    booking = models.InterviewBooking(
        name=name,
        email=email,
        interview_date=interview_date,
        time_slot=time_slot,
        notes=notes
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_bookings(db: Session, email: str = None) -> List[models.InterviewBooking]:
    query = db.query(models.InterviewBooking)
    if email:
        query = query.filter_by(email=email)
    return query.order_by(models.InterviewBooking.interview_date).all()

