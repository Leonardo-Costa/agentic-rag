import logging
import os
from typing import List, Tuple
import uuid
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        logger.info("Initializing EmbeddingService...")
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        collection_name = os.getenv('COLLECTION_NAME', 'agentic_rag_embeddings')
        db_user = os.getenv("DB_USER", "myuser")
        db_password = os.getenv("DB_PASSWORD", "mypassword")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "postgres")
        
        connection = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        logger.debug(f"Connecting to PGVector with collection: {collection_name}")
        self.vector_store = PGVector(
            embeddings=embeddings,
            collection_name=collection_name,
            connection=connection,
            use_jsonb=True,
        )
        logger.info("EmbeddingService initialized.")

    def chunk_documents(self, documents: list[Document]) -> list[Document]:
        logger.info(f"Chunking {len(documents)} documents...")
        chunk_size = int(os.getenv("CHUNK_SIZE", 1000))
        chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 200))

        md_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.MARKDOWN,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        all_chunks = []

        for i, document in enumerate(documents):
            chunks = md_splitter.create_documents([document.page_content])
            logger.debug(f"Document {i+1}/{len(documents)}: {document.metadata.get('file_name', 'unknown')} - {document.metadata.get('page_number', 'unknown')} - {len(chunks)} chunks created.")

            chunks = [Document(page_content=chunk.page_content, metadata=document.metadata) for chunk in chunks]
            all_chunks.extend(chunks)
        
        logger.debug(f"Created {len(all_chunks)} chunks from {len(documents)} documents.")
       
        return all_chunks

    def add_documents(self, documents: list[Document]) -> int:
        logger.info(f"Adding {len(documents)} documents to vector store...")
        chunks = self.chunk_documents(documents)
        self.vector_store.add_documents(
            chunks,
            ids=[uuid.uuid4().hex for _ in chunks]
        )
        logger.info(f"Added {len(chunks)} chunks to vector store.")

        return len(chunks)

    def query_document(self, query: str, top_k: int = 5) -> list[Document]:
        threshold = float(os.getenv("SIMILARITY_THRESHOLD", 0.7))

        logger.info(f"Querying vector store with: '{query}' (top_k={top_k})")
        results: List[Tuple[Document, float]] = self.vector_store.similarity_search_with_score(query, k=top_k)

        logger.info(f"Found {len(results)} results before applying threshold of {threshold}.")

        results = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc, score in results if score >= threshold
        ]

        logger.debug(f"Filtered results to {len(results)} documents after applying threshold.")

        logger.info(f"Query returned {len(results)} results.")
        return results