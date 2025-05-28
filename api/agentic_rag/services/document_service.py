from pathlib import Path
from typing import Any, Dict, List
from agentic_rag.services.ocr_service import OCRService
from langchain_core.documents import Document
import os
import logging

from fastapi import HTTPException, UploadFile
from agentic_rag.services.temporary_file_service import TemporaryFileService
from agentic_rag.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class DocumentProcessingService:
    def __init__(
        self, 
        temp_file_service: TemporaryFileService, 
        ocr_service: OCRService,
        embedding_service: EmbeddingService,
        max_file_size: int = 50 * 1024 * 1024
    ):
        self.temp_file_service = temp_file_service
        self.ocr_service = ocr_service
        self.embedding_service = embedding_service
        self.max_file_size = max_file_size
        self.allowed_extensions = {'.pdf'}
        logger.debug(
            "DocumentProcessingService initialized with max_file_size=%d and allowed_extensions=%s",
            self.max_file_size,
            self.allowed_extensions
        )

    async def process_uploaded_documents(self, files: List[UploadFile]) -> Dict[str, Any]:
        if not files:
            logger.warning("No files uploaded")
            raise HTTPException(status_code=400, detail="No files uploaded")
        
        documents_indexed = 0
        total_chunks = 0
        temp_files_in_batch = []
 
        logger.info("Starting document processing for %d files", len(files))

        async with self.temp_file_service.temp_batch_dir_context() as batch_temp_dir:
            logger.debug("Temporary batch directory created: %s", batch_temp_dir)
            try:
                for file in files:
                    logger.debug("Processing file: %s", file.filename)
                    self._validate_file(file)
                    
                    temp_file_path = os.path.join(batch_temp_dir, file.filename)
                    temp_files_in_batch.append(temp_file_path)

                    logger.debug("Saving uploaded file to temporary path: %s", temp_file_path)
                    await self.temp_file_service.save_uploaded_file(file, temp_file_path)
                    logger.info("File saved to temporary path: %s", temp_file_path)
                    
                    logger.debug("Starting OCR processing for file: %s", temp_file_path)
                    processed_documents: list[Document] = await self.ocr_service.process_document_with_ocr(temp_file_path)
                    
                    logger.info("OCR processing completed for file: %s", file.filename)

                    number_of_chunks = self.embedding_service.add_documents(processed_documents)


                    logger.info("Documents added to embedding service for file: %s", file.filename)

                    total_chunks += number_of_chunks
                    documents_indexed += 1
                    
            except HTTPException as e:
                logger.error("HTTPException during document processing: %s", e.detail)
                raise
            except Exception as e:
                logger.exception("An error occurred during document processing")
                raise HTTPException(
                    status_code=500, 
                    detail=f"Error processing documents: {str(e)}"
                )
            finally:
                logger.debug("Cleaning up temporary files in batch: %s", temp_files_in_batch)
            
        logger.info("Document processing completed successfully")
        return {
            "message": "Documents processed successfully",
            "documents_indexed": documents_indexed,
            "total_chunks": total_chunks
        }
    
    def _validate_file(self, file: UploadFile) -> None:
        if not file.filename:
            logger.warning("File validation failed: No filename provided")
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in self.allowed_extensions:
            logger.warning("File validation failed: Invalid file extension for %s", file.filename)
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} must be a PDF file (allowed: {', '.join(self.allowed_extensions)})"
            )
        
        if hasattr(file, 'size') and file.size is not None and file.size > self.max_file_size:
            logger.warning("File validation failed: File %s is too large", file.filename)
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is too large. Maximum size: {self.max_file_size // (1024*1024)}MB"
            )
        logger.debug("File validation passed for: %s", file.filename)