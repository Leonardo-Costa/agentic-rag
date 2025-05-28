import logging
import os
from typing import List
from pyzerox import zerox
from pyzerox.core.types import ZeroxOutput
from langchain_core.documents import Document

logger = logging.getLogger(__name__)


class OCRService:
    async def process_document_with_ocr(self, file_path: str) -> List[Document]:
        logger.info(f"Starting OCR processing for file: {file_path}")
        model = os.getenv('OCR_MODEL', 'gpt-4o-mini')
        logger.debug(f"Using OCR model: {model}")

        try:
            pages: ZeroxOutput = await zerox(file_path=file_path, model=model)
            logger.info(f"OCR processing completed for file: {file_path}")
        except Exception as e:
            logger.error(f"OCR processing failed for file: {file_path} with error: {e}")
            raise

        documents = [
            Document(
                page_content=page.content,
                metadata={
                    'file_name': pages.file_name,
                    'page_number': page.page
                }
            ) for page in pages.pages
        ]
        logger.debug(f"Created {len(documents)} Document objects from OCR output for file: {file_path}")

        return documents
