# RagaVerse - System Architecture

## 1. Frontend

React + TypeScript + Vite + Tailwind CSS

Responsibilities:
- Dashboard
- AI Assistant
- Raga Explorer
- Audio Analysis
- Vocal Coach
- Composition Studio
- Practice Planner

## 2. Backend

Python 3.11 + FastAPI

Responsibilities:
- API management
- Business logic
- Authentication
- AI service integration
- Audio processing
- Database operations

## 3. AI Architecture

- OpenAI API
- LangChain
- LangGraph
- Tool Calling
- Structured Outputs
- Multi-Agent Orchestration

## 4. Knowledge Architecture

- Document ingestion
- Text extraction
- Chunking
- Embeddings
- Qdrant
- Retrieval
- Reranking
- Grounded generation

## 5. Audio Intelligence

- Librosa
- NumPy
- SciPy
- SoundFile
- PyTorch

## 6. Storage

- PostgreSQL: Application data
- Qdrant: Vector embeddings
- Redis: Caching and background tasks

## 7. Deployment

- Docker
- Docker Compose
- Cloud hosting
- CI/CD

## Architectural Principle

Build a modular monolith first.
Introduce agent orchestration and
independent deployment boundaries
only when justified.