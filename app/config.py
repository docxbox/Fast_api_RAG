import os

class Settings:
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    MAX_TURNS = int(os.getenv("MAX_TURNS", "10"))
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

settings = Settings()
