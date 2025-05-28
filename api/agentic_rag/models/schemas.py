from typing import List
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str

class Chunk(BaseModel):
    file_name: str
    page_number: int
    content: str

class AnswerResponse(BaseModel):
    answer: str
    chunks: List[Chunk]

class AddDocumentResponse(BaseModel):
    message: str
    documents_indexed: int

class DocumentUploadResponse(BaseModel):
    message: str
    documents_indexed: int
    total_chunks: int

class DocumentRequest(BaseModel):
    page_content: str
    metadata: dict

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
