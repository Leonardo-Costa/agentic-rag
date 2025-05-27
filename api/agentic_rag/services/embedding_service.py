import os
import uuid
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document


class EmbeddingService:
    def __init__(self):
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        collection_name = os.getenv('COLLECTION_NAME', 'agentic_rag_embeddings')
        db_user = os.getenv("DB_USER", "myuser")
        db_password = os.getenv("DB_PASSWORD", "mypassword")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "postgres")
        
        connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        print('\n\n\n\n\n')
        print(connection)

        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection,
            use_jsonb=True,
        )

    def add_documents(self, documents: list[Document]) -> None:
        self.vector_store.add_documents(documents, ids=[uuid.uuid4().hex for _ in documents])

    def query_document(self, query: str, top_k: int = 5) -> list[Document]:
        results = self.vector_store.similarity_search(query, k=top_k)
        return results
