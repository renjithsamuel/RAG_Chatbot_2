from fastapi import APIRouter
from app.models.schemas import ChatRequest, ChatResponse
from app.services.llm_service import LLMService
from app.services.vector_store import VectorStoreManager

router = APIRouter()
vector_manager = VectorStoreManager()
llm_service = None  # Will be initialized after vector store

@router.post("/ask", response_model=ChatResponse)
async def ask_question(request: ChatRequest):
    global llm_service
    if not llm_service:
        retriever = vector_manager.get_retriever()
        llm_service = LLMService(retriever)
    response = llm_service.query(request.question)
    return ChatResponse(answer=response)