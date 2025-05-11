from fastapi import FastAPI
from app.routes.chat import router as chat_router
from app.routes.ingest import router as ingest_router
from app.config import settings

app = FastAPI(title="RAG Chatbot", version="0.1.0")
app.include_router(chat_router, prefix="/api/v1")
app.include_router(ingest_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    # Initialize vector store here if pre-loading documents
    pass