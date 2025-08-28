from qdrant_client import QdrantClient, models
from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class QdrantClientWrapper:
    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)

    def connect(self):
        # The client is already connected in the constructor
        pass

    def upsert_vector(self, vector_id: str, vector: list[float], payload: dict):
        self.client.upsert(
            collection_name="documents",
            points=[
                models.PointStruct(
                    id=vector_id,
                    vector=vector,
                    payload=payload,
                )
            ],
            wait=True,
        )

    def semantic_search(self, query: str, top_k: int) -> list[str]:
        response = client.embeddings.create(
            input=query,
            model="text-embedding-3-small",
            encoding_format="float"
        )
        query_vector = response.data[0].embedding

        search_result = self.client.search(
            collection_name="documents",
            query_vector=query_vector,
            limit=top_k,
        )

        return [hit.payload["chunk"] for hit in search_result]