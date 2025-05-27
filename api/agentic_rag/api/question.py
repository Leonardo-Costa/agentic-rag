from typing import List
from fastapi import APIRouter, Depends
from agentic_rag.models.schemas import QuestionRequest, AnswerResponse
from agentic_rag.services.embedding_service import EmbeddingService
from langchain_core.documents import Document

router = APIRouter()

def get_embedding_service():
    return EmbeddingService()


@router.post("/question", response_model=AnswerResponse)
def ask_question(payload: QuestionRequest, service=Depends(get_embedding_service)):
    response: List[Document] = service.query_document(payload.question, top_k=5)
    return AnswerResponse(answer=" ".join([doc.page_content for doc in response]))

