from fastapi import APIRouter, Depends
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreManager# Will be initialized after vector store

router = APIRouter()

def get_vector_manager():
    return VectorStoreManager()

def get_llm_service(vector_manager: VectorStoreManager = Depends(get_vector_manager)):
    return LLMService(vector_manager.get_retriever())

@router.post("/ask", response_model=ChatResponse)
async def ask_question(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    response = llm_service.query(request.question)
    return ChatResponse(answer=response)