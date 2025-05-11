from langchain_community.document_loaders import PyPDFLoader, TextLoader
from typing import List, Union
from langchain.schema import Document

class DocumentLoader:
    @staticmethod
    def load_documents(file_path: str) -> List[Document]:
        if file_path.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith(".txt"):
            loader = TextLoader(file_path)
        else:
            raise ValueError("Unsupported file format")
        return loader.load()

    @staticmethod
    def split_documents(documents: List[Document], chunk_size: int, chunk_overlap: int) -> List[Document]:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        return text_splitter.split_documents(documents)