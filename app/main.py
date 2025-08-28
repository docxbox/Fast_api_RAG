from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import database
from routers import ingest, rag
from core.memory import RedisChatMemory


app = FastAPI(
    title="Palm Mind RAG API",
    description="Document ingestion & conversational RAG backend",
    version="1.0.0"
)

#CORS 
origins = [
    "*",  # change to allowed origins 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from core.memory import RedisChatMemory

redis_chat_memory = RedisChatMemory()

#Event Handlers 
@app.on_event("startup")
def startup_event():

    #Initialize Postgres tables
    database.Base.metadata.create_all(bind=database.engine)
    print("Postgres tables created.")

    #Connect to Redis
    redis_chat_memory.connect()
    print("Redis connected.")

    #Connect to Qdrant
    from core.qdrant_client import QdrantClientWrapper
    QdrantClientWrapper().connect()
    print("Qdrant connected.")

@app.on_event("shutdown")
def shutdown_event():
    redis_chat_memory.close()
    print("Redis disconnected.")


#Routers 
app.include_router(ingest.router)
app.include_router(rag.router)


#Health Check 
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is running"}


