from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.core.config import settings
from app.services.rag import RAGService

app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    # Disable docs in production for security
    openapi_url=f"{settings.api_prefix}/openapi.json" if not settings.production_mode else None,
    docs_url=f"{settings.api_prefix}/docs" if not settings.production_mode else None,
    redoc_url=f"{settings.api_prefix}/redoc" if not settings.production_mode else None,
)

rag_service = RAGService()

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500) # Limit query length
    top_k: int = Field(3, ge=1, le=10) # Limit top_k to reasonable range

class SearchResponse(BaseModel):
    results: List[str]

class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000) # Limit question length

class AskResponse(BaseModel):
    answer: str

@app.get("/")
async def root():
    return {"message": "Cambodia DPL Navigator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post(f"{settings.api_prefix}/search", response_model=SearchResponse)
async def search_documents(request: SearchRequest):
    # TODO: Implement actual document search (retrieval only, not RAG query)
    # For now, this will just return a mock or use the RAG query for simplicity
    # A dedicated search function in RAGService would be better for pure retrieval
    mock_results = [f"Mock search result for: {request.query}"]
    return SearchResponse(results=mock_results)

@app.post(f"{settings.api_prefix}/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    answer = await rag_service.query(request.question)
    if "Error:" in answer:
        raise HTTPException(status_code=500, detail=answer)
    return AskResponse(answer=answer)
