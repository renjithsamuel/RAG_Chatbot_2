from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.document_loader import DocumentLoader
from app.services.vector_store import VectorStoreManager
from app.config import settings
import os
import uuid

router = APIRouter(tags=["Ingestion"])
vector_manager = VectorStoreManager()

UPLOAD_DIR = "app/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    return await process_file(file, "pdf")

@router.post("/ingest/text")
async def ingest_text(file: UploadFile = File(...)):
    return await process_file(file, "txt")

async def process_file(file: UploadFile, file_type: str):
    if not file.filename:
        raise HTTPException(400, "No file uploaded")
    
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.{file_type}"
    
    # Save file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Process documents
    try:
        documents = DocumentLoader.load_documents(file_path)
        splits = DocumentLoader.split_documents(
            documents=documents,
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        vector_manager.add_documents(splits)
        return {"status": "success", "message": f"{len(splits)} chunks added"}
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")