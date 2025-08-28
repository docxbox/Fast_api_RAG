from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uuid
import os

from core import database, crud
from core.utils.pdf import pdf_extract
from core.utils.txt import txt_extract
from core.chunking import chunk_text  # your chunking strategies
from core.embeddings import generate_embeddings as get_embedding  # embedding function
from core.qdrant_client import QdrantClientWrapper  # wrapper for Qdrant operations

router = APIRouter(prefix="/ingest", tags=["Document Ingestion"])

qdrant_client = QdrantClientWrapper()  # initialize once, reuse

# ----------------- Upload Endpoint -----------------
@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    chunk_strategy: str = "simple",  # selectable strategy
    db: Session = Depends(database.get_db)
):
    # Validate file type
    if not file.filename.endswith((".pdf", ".txt")):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are allowed.")

    # Save uploaded file temporarily
    file_id = str(uuid.uuid4())
    temp_path = f"/tmp/{file_id}_{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    # Extract text
    try:
        if file.filename.endswith(".pdf"):
            text = pdf_extract(temp_path)
        else:
            text = txt_extract(temp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {e}")
    finally:
        os.remove(temp_path)

    if not text.strip():
        raise HTTPException(status_code=400, detail="No text extracted from file.")

    # Chunk text
    chunks = chunk_text(text, strategy=chunk_strategy)
    if not chunks:
        raise HTTPException(status_code=500, detail="Chunking failed.")

    # Generate embeddings
    vector_ids = []
    for chunk in chunks:
        embedding_vector = get_embedding(chunk)  # returns List[float]
        vec_id = str(uuid.uuid4())
        # Upsert into Qdrant
        qdrant_client.upsert_vector(vector_id=vec_id, vector=embedding_vector, payload={"chunk": chunk})
        vector_ids.append(vec_id)

    # Save metadata in Postgres
    crud.save_document_metadata(
        db=db,
        file_name=file.filename,
        chunks=chunks,
        vector_ids=vector_ids,
        chunk_strategy=chunk_strategy,
        additional_metadata={"uploaded_by": "system"}  # optional
    )

    return JSONResponse(
        status_code=200,
        content={
            "message": f"File '{file.filename}' ingested successfully.",
            "total_chunks": len(chunks),
            "vector_ids": vector_ids
        }
    )