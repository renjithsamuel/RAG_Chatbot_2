import os
from xml.dom.minidom import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.config import settings

class VectorStoreManager:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL
        )
        self.vector_store = None
        self.vector_store_path = "app/data/vector_store/faiss_index"
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(self.vector_store_path), exist_ok=True)
        
        # Only load if index files exist
        if self._index_exists():
            self.vector_store = FAISS.load_local(
                self.vector_store_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
    def _initialize_empty_store(self):
        """Create empty vector store with dummy content"""
        dummy_docs = [
            Document(
                page_content="Initial document",
                metadata={"source": "system"}
            )
        ]
        self.create_vector_store(dummy_docs)
        print("Created new vector store with dummy document")
        
    def _index_exists(self):
        return os.path.exists(f"{self.vector_store_path}/index.faiss")

    def create_vector_store(self, documents):
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        self._save_vector_store()
        return self.vector_store

    def add_documents(self, documents):
        if not self.vector_store:
            self.create_vector_store(documents)
        else:
            self.vector_store.add_documents(documents)
            self._save_vector_store()

    def _save_vector_store(self):
        if self.vector_store:
            self.vector_store.save_local(self.vector_store_path)

    def get_retriever(self, k: int = 3):
        if not self.vector_store:
            self._initialize_empty_vector_store()
            
        return self.vector_store.as_retriever(search_kwargs={"k": k})
    
    def _initialize_empty_store(self):
        """Create empty vector store if none exists"""
        self.vector_store = FAISS.from_texts(
            texts=["Initial document"],
            embedding=self.embeddings
        )
        self._save_vector_store()