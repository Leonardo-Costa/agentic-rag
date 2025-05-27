from fastapi import APIRouter, Depends
from agentic_rag.models.schemas import AnswerResponse, DocumentRequest
from agentic_rag.services.embedding_service import EmbeddingService
from langchain_core.documents import Document

router = APIRouter()

def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

@router.post("/add_document", response_model=AnswerResponse)
def add_document(payload: DocumentRequest, service=Depends(get_embedding_service)):
    service.add_documents([Document(page_content=payload.page_content, metadata=payload.metadata)])
    
    return AnswerResponse(answer="foi")
