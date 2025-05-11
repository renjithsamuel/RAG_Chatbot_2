from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from app.config import settings

class LLMService:
    def __init__(self, retriever):
        self.llm = Ollama(
            model=settings.MODEL_NAME,
            temperature=0,
            num_gpu=1  # Utilize GPU
        )
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )

    def query(self, question: str) -> str:
        result = self.qa_chain.invoke({"query": question})
        return result["result"]