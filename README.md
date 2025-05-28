# agentic-rag

A FastAPI-based retrieval-augmented generation (RAG) service for PDF documents. It leverages OpenAI embeddings, PGVector (PostgreSQL vector extension), and pyzerox for OCR to provide semantic search and Q&A capabilities over uploaded documents.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Upload Documents](#upload-documents)
  - [Add Document via API](#add-document-via-api)
  - [Ask a Question](#ask-a-question)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Features

- **PDF Ingestion & OCR**: Upload PDF files and extract text using GPT-powered OCR (pyzerox).
- **Text Chunking**: Split documents into overlapping chunks using Langchain text splitter.
- **Embeddings & Vector Store**: Embed text chunks with OpenAI embeddings and store in PostgreSQL via PGVector.
- **Semantic Search & Q&A**: Perform similarity-based retrieval and answer questions using semantic search.
- **RESTful API**: Exposes endpoints for document ingestion, embedding, and querying.
- **Dockerized**: Easily deploy with Docker Compose (Postgres + API service).

## Architecture

```text
[ PDF Upload ] --> [ OCRService ] --> [ Text Chunks ] --> [ EmbeddingService ] --> [ PGVector DB ]
                                                          ^
                                                          |
[ Question API ] ------------------------------------------
```

## Prerequisites

- [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
- [OpenAI API Key](https://platform.openai.com/)
- (Optional) Python 3.12 for local development

## Configuration

Create a `.env` file in the project root to configure environment variables:

```dotenv
# OpenAI & RAG
OPENAI_API_KEY=your_openai_api_key

# PostgreSQL / PGVector
DB_HOST=localhost
DB_PORT=5432
DB_USER=myuser
DB_PASSWORD=mypassword
DB_NAME=postgres
COLLECTION_NAME=agentic_rag_embeddings

# Text splitting
CHUNK_SIZE=1000
CHUNK_OVERLAP=200

# OCR model (pyzerox)
OCR_MODEL=gpt-4o-mini

# (Optional) Temporary files directory
TEMP_DIR=/tmp

# Application log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_LEVEL=DEBUG
```

> **Note**: `.env` is gitignored; do not commit your secrets.

## Getting Started

### Using Docker Compose

1. Ensure your `.env` file is set up as above.
2. Launch the Postgres & API services:

   ```bash
   docker-compose up --build
   ```

3. The API will be available at `http://localhost:8001`.

### Local Development (without Docker)

```bash
# Navigate to the API source directory
cd api

# (Optional) Install UV (fast env & dependency manager)
curl -fsSL https://astral.sh/uv/install.sh | sh

# Create & activate virtual environment via UV
uv venv
uv sync --locked

# Start the FastAPI server with live reload
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

Alternatively, using pip:

```bash
cd api
python3 -m venv .venv
source .venv/bin/activate
pip install .
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## Usage

### Upload Documents

Upload one or more PDF files for OCR processing and embedding:

```bash
curl -X POST "http://localhost:8001/documents" \
  -F "files=@/path/to/doc1.pdf" \
  -F "files=@/path/to/doc2.pdf"
```

### Add Document via API

Add raw text content directly to the vector store:

```bash
curl -X POST "http://localhost:8001/add_document" \
  -H "Content-Type: application/json" \
  -d '{
    "page_content": "Your document text here",
    "metadata": {"source": "manual"}
}'
```

### Ask a Question

Perform a semantic search and retrieve an answer from indexed documents:

```bash
curl -X POST "http://localhost:8001/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the main topic of the documents?"}'
```

## API Documentation

Interactive API docs are available once the server is running:

- Swagger UI: [http://localhost:8001/docs](http://localhost:8001/docs)
- ReDoc: [http://localhost:8001/redoc](http://localhost:8001/redoc)

## Project Structure

```
.
├── api/                   # FastAPI application
│   ├── agentic_rag/       # Core modules: API routers, services, models
│   ├── Dockerfile         # Docker image for the API service
│   ├── main.py            # FastAPI app initialization
│   ├── pyproject.toml     # Dependencies & package metadata
│   └── uv.lock            # Locked dependencies (UV)
├── docker-compose.yaml    # Postgres (pgvector) + API service
├── .env                   # Environment variables (gitignored)
├── uploads/               # (Optional) directory for persisted files/public assets
└── README.md              # Project documentation (this file)
```

## Development

- Code is organized with clear separation between API routers, Pydantic schemas, and service classes.
- Document ingestion pipeline:
  - `DocumentProcessingService` handles PDF validation, temporary storage, OCR, and bulk embedding.
  - `OCRService` uses pyzerox for page-wise content extraction.
  - `EmbeddingService` splits texts into chunks and stores embeddings in PGVector.
- For changes to dependencies, update `pyproject.toml` and lock via UV (`uv lock`) or rebuild Docker image.

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or issue.

## License

This project does not include a license. Please contact the maintainers for licensing information.