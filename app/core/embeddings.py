from typing import List, Dict
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from openai import OpenAI
import uuid

from app.config import settings

openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

qdrant_client = QdrantClient(url=settings.QDRANT_URL)

COLLECTION_NAME = "documents"

def init_collection(vector_size: int = 1535):
    """ Initialize Qdrant collection for storing embeddings """
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )


def generate_embeddings(chunks: list[str], model: str = "text-embedding-3-small") -> list[list[float]]:
    """ Generate embeddings for a list of text chunks using OpenAI """
    response = openai_client.embeddings.create(
        input=chunks,
        model=model,
        encoding_format="float"
    )
    return [item.embedding for item in response.data]



def store_embeddings(chunks: list[str], metadata: Dict = None,
                     model: str = "text-embedding-3-small") -> list[str]:
    """ Generate and store embeddings in Qdrant """
    embeddings = generate_embeddings(chunks, model=model)
    vector_ids = [str(uuid.uuid4()) for _ in chunks]
    points = [
        PointStruct(
            id=vector_ids[i],
            vector=embeddings[i],
            payload={"text": chunks[i], **(metadata or {})}
        ) for i in range(len(chunks))
    ]
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )
    return vector_ids