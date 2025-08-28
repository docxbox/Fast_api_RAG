# ✦ FastAPI RAG

**FastAPI RAG** is a Retrieval-Augmented Generation (RAG) application built using FastAPI. It integrates large language models (LLMs), PostgreSQL, and a Qdrant vector database to enable intelligent question answering based on your own PDF documents.

---

## 📖 Description

This application allows you to upload PDF documents, process and chunk them, generate embeddings, and store them for efficient retrieval. When a user asks a question, the system retrieves the most relevant document chunks and uses an LLM (like OpenAI's GPT models) to generate an accurate, context-aware answer.

---

## 🚀 Features

- 📄 **PDF Ingestion**: Upload and process PDF documents.
- ✂️ **Document Chunking**: Split documents into manageable chunks.
- 🧠 **Embeddings Generation**: Generate embeddings using OpenAI models.
- 📦 **Vector Storage**: Store embeddings in a Qdrant vector database.
- ❓ **Question Answering**: Ask questions based on ingested documents using the RAG technique.
- 💬 **Conversation Memory**: Maintain dialogue context to support follow-up questions.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn  
- **Database**: PostgreSQL (SQLAlchemy, psycopg2)  
- **Vector Database**: Qdrant  
- **LLM & Embeddings**: OpenAI API  
- **PDF Parsing**: PyMuPDF  
- **Caching**: Redis  

---

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Fast-api_RAG.git
cd Fast-api_RAG
```
### 2. Create and activate a virtual environment
  ``` python -m venv .venv
      source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Set up environment variables

```
DATABASE_URL=postgresql://user:password@host:port/database
OPENAI_API_KEY=your-openai-api-key
QDRANT_URL=your-qdrant-url
QDRANT_API_KEY=your-qdrant-api-key
REDIS_HOST=your-redis-host
REDIS_PORT=your-redis-port

```

### 🚀 Usage
Run the application
uvicorn app.main:app --reload







