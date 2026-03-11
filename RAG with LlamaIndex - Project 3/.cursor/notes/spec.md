# System Technical Specification

## Overview
RAG (Retrieval-Augmented Generation) system built with LlamaIndex for intelligent document querying and retrieval.

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/ui
- **State Management**: React Context + Hooks

### Backend
- **API Layer**: Next.js API Routes
- **Database**: PostgreSQL with Prisma ORM
- **Vector Store**: LlamaIndex with ChromaDB
- **LLM Integration**: OpenAI GPT-4 / GPT-3.5-turbo

### Infrastructure
- **ORM**: Prisma
  - Schema-first approach
  - Type-safe database queries
  - Migration management
- **Database**: PostgreSQL 15+
  - JSONB support for metadata storage
  - Full-text search capabilities
  - Vector extension for embeddings

## Architecture

### Data Flow
1. Document ingestion → Text splitting → Embedding generation
2. Vector storage in ChromaDB with metadata in PostgreSQL
3. Query processing → Vector similarity search → Context retrieval
4. LLM response generation with retrieved context

### Key Components
- **Document Processor**: Handles PDF, TXT, DOCX parsing
- **Embedding Service**: Generates vector embeddings via OpenAI
- **Query Engine**: LlamaIndex query interface
- **Response Synthesizer**: Combines retrieved context with LLM

## API Endpoints
- `POST /api/upload` - Document upload and processing
- `POST /api/query` - RAG query execution
- `GET /api/documents` - List indexed documents
- `DELETE /api/documents/:id` - Remove document from index

## Environment Variables
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

---
*Last updated by AI Agent - 2024*
