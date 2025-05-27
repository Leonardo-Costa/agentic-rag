import os
from typing import List
from pyzerox import zerox
from pyzerox.core.types import ZeroxOutput
from langchain_core.documents import Document


class OCRService:
    async def process_document_with_ocr(self, file_path: str) -> List[Document]:
        model = os.getenv('OCR_MODEL', 'gpt-4o-mini')

        pages: ZeroxOutput = await zerox(file_path=file_path, model=model)

        documents = [
            Document(
                page_content=page.content,
                metadata={
                    'file_name': pages.file_name,
                    'page_number': page.page
                }
            ) for page in pages.pages
        ]

        return documents

