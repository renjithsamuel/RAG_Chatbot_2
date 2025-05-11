import os
from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.ingest import router as ingest_router
from app.config import settings
from app.services.vector_store import VectorStoreManager

app = FastAPI(title="RAG Chatbot", version="0.1.0")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize necessary directories
    os.makedirs("app/data/uploads", exist_ok=True)
    os.makedirs("app/data/vector_store", exist_ok=True)
    
    # Initialize empty vector store if none exists
    vector_manager = VectorStoreManager()
    if not vector_manager.vector_store:
        print("Initializing new vector store...")
        # Create empty store with dummy text
        vector_manager._initialize_empty_store()
    print("Vector store ready")