from pydantic import BaseModel
from langchain_core.documents import Document

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

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
