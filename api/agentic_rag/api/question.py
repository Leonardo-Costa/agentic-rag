import logging
import os
from typing import List
from fastapi import APIRouter, Depends
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from agentic_rag.models.schemas import Chunk, QuestionRequest, AnswerResponse
from agentic_rag.services.embedding_service import EmbeddingService
from langchain_core.documents import Document

router = APIRouter()
logger = logging.getLogger(__name__)

def get_embedding_service():
    return EmbeddingService()

def get_llm_service():
    return ChatOpenAI(
        model_name=os.getenv("LLM_MODEL", "gpt-4o-mini"),
        temperature=float(os.getenv("LLM_TEMPERATURE", 0.7)),
        openai_api_key=os.getenv("OPENAI_API_KEY", None),
        base_url=os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1"),
    )

@router.post("/question", response_model=AnswerResponse)
def ask_question(
    payload: QuestionRequest,
    embedding_service=Depends(get_embedding_service),
    llm_service=Depends(get_llm_service),
):
    top_k = int(os.getenv("TOP_K", 5))
    top_documents: List[Document] = embedding_service.query_document(payload.question, top_k=top_k)

    if not top_documents:
        return AnswerResponse(answer="No relevant documents found.", chunks=[])

    context = "\n\n".join([doc.page_content for doc in top_documents])

    logger.info(f"Context for question '{payload.question}': {context[:100]}...")
    logger.info(f"Found {len(top_documents)} relevant documents for question '{payload.question}'")

    messages = [
        SystemMessage(content="Você é um assistente especializado em responder perguntas com base no contexto fornecido."),
        HumanMessage(content=f"Contexto:\n{context}\n\nPergunta: {payload.question}")
    ]

    response = llm_service.invoke(messages)

    return AnswerResponse(
        answer=response.content,
        chunks=[
            Chunk(
                file_name=doc.metadata.get("file_name", "unknown"),
                page_number=doc.metadata.get("page_number", 0),
                content=doc.page_content,
            )
            for doc in top_documents
        ],
    )
