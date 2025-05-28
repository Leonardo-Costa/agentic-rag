from fastapi import APIRouter, Depends, UploadFile, File
from typing import List

from agentic_rag.models.schemas import DocumentUploadResponse
from agentic_rag.services.document_service import DocumentProcessingService
from agentic_rag.services.ocr_service import OCRService
from agentic_rag.services.temporary_file_service import TemporaryFileService
from agentic_rag.services.embedding_service import EmbeddingService


router = APIRouter()

def get_file_parsing_service() -> DocumentProcessingService:
    return DocumentProcessingService(
        temp_file_service=TemporaryFileService(),
        ocr_service=OCRService(),
        embedding_service=EmbeddingService(),
        max_file_size=50 * 1024 * 1024
    )

@router.post("/documents", response_model=DocumentUploadResponse)
async def upload_documents(files: List[UploadFile] = File(...), service: DocumentProcessingService = Depends(get_file_parsing_service)):
    response = await service.process_uploaded_documents(files)

    return DocumentUploadResponse(
        message=response.message,
        documents_indexed=response.documents_indexed,
        total_chunks=response.total_chunks
    )
