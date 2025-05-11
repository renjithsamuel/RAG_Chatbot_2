import os
from app.services.document_loader import DocumentLoader
from app.services.vector_store import VectorStoreManager
from app.config import settings

def main():
    # Load documents
    documents = DocumentLoader.load_documents("app/data/sample_docs.pdf")
    
    # Split documents
    splits = DocumentLoader.split_documents(
        documents=documents,
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    
    # Create vector store
    vector_manager = VectorStoreManager()
    vector_manager.create_vector_store(splits)
    print("Vector store created successfully!")

if __name__ == "__main__":
    main()