from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from core import database, crud
from core.memory import RedisChatMemory  # your Redis memory wrapper
from core.qdrant_client import QdrantClientWrapper  # your Qdrant client
from core.llm import generate_answer  # your LLM wrapper using embeddings & context

router = APIRouter(prefix="/rag", tags=["Conversational RAG"])

qdrant_client = QdrantClientWrapper()
chat_memory = RedisChatMemory()

# ----------------- Pydantic Schemas -----------------
class ChatRequest(BaseModel):
    user_id: str
    query: str
    max_results: int = 3

class ChatResponse(BaseModel):
    answer: str
    context_chunks: List[str]

class BookingRequest(BaseModel):
    name: str
    email: EmailStr
    interview_date: datetime
    time_slot: str
    notes: Optional[str] = None

class BookingResponse(BaseModel):
    message: str
    booking_id: int


# ----------------- Chat Endpoint -----------------
@router.post("/query", response_model=ChatResponse)
def query_rag(request: ChatRequest, db: Session = Depends(database.get_db)):
    """
    Multi-turn RAG query:
    - Retrieves relevant chunks from Qdrant
    - Maintains conversation context in Redis
    - Generates answer via LLM
    """
    # Fetch previous conversation from Redis
    history = chat_memory.get_history(user_id=request.user_id)

    # Retrieve relevant chunks from Qdrant
    try:
        chunks = qdrant_client.semantic_search(
            query=request.query,
            top_k=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search failed: {e}")

    # Combine context + query for LLM
    answer = generate_answer(query=request.query, context=chunks, history=history)

    # Save the interaction to Redis memory
    chat_memory.add_message(user_id=request.user_id, query=request.query, answer=answer)

    return ChatResponse(answer=answer, context_chunks=chunks)


# ----------------- Interview Booking Endpoint -----------------
@router.post("/book", response_model=BookingResponse)
def book_interview(request: BookingRequest, db: Session = Depends(database.get_db)):
    """
    Save interview booking to Postgres
    """
    booking = crud.save_booking(
        db=db,
        name=request.name,
        email=request.email,
        interview_date=request.interview_date,
        time_slot=request.time_slot,
        notes=request.notes
    )

    return BookingResponse(
        message=f"Interview booked successfully for {request.name} on {request.interview_date.date()} at {request.time_slot}.",
        booking_id=booking.id
    )



@router.get("/bookings", response_model=List[BookingResponse])
def get_user_bookings(email: Optional[str] = None, db: Session = Depends(database.get_db)):
    bookings = crud.get_bookings(db=db, email=email)
    response = [
        BookingResponse(
            message=f"Interview booked for {b.name} on {b.interview_date.date()} at {b.time_slot}",
            booking_id=b.id
        )
        for b in bookings
    ]
    return response