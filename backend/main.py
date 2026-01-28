"""
AI Multi-Engine Search System - Backend API
Orchestrates parallel searches across 5 search engines with AI synthesis.
With JWT authentication for security.
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import json
from datetime import datetime, timedelta
import jwt
import os

from config import settings
from query_processor import QueryProcessor
from search_orchestrator import SearchOrchestrator
from result_synthesizer import ResultSynthesizer

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-12345!")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
DEFAULT_API_KEY = os.getenv("API_KEY", "nexus-ai-search-default-key")

security = HTTPBearer()


app = FastAPI(
    title="AI Search Engine API",
    description="Multi-engine AI search with intelligent result synthesis",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
query_processor = QueryProcessor()
search_orchestrator = SearchOrchestrator()
result_synthesizer = ResultSynthesizer()


class LoginRequest(BaseModel):
    """Login request model."""
    api_key: str


class TokenResponse(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str
    expires_in: int


class SearchRequest(BaseModel):
    """Search request model."""
    query: str
    max_results: Optional[int] = 15


class SearchResponse(BaseModel):
    """Search response model."""
    query: str
    sub_queries: List[str]
    results: List[Dict[str, Any]]
    summary: str
    engine_stats: Dict[str, Any]
    processing_time: float


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthCredentials = Depends(security)) -> str:
    """Verify JWT token."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
async def root():
    """API root endpoint - Public."""
    return {
        "name": "AI Search Engine API",
        "version": "1.0.0",
        "status": "operational",
        "engines": ["SearXNG", "DuckDuckGo", "Qwant", "Wikipedia", "Wikidata"],
        "security": "JWT Bearer Token Required for /search endpoint"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint - Public."""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """
    Login endpoint - Get JWT token using API key.
    
    Default API Key: nexus-ai-search-default-key
    
    You can change it by setting the API_KEY environment variable.
    """
    if request.api_key != DEFAULT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "nexus-user"},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest, token: str = Depends(verify_token)):
    """
    Perform multi-engine AI search.
    
    Process:
    1. Break down query into sub-queries
    2. Execute parallel searches across 5 engines
    3. Synthesize results into super output
    """
    start_time = asyncio.get_event_loop().time()
    
    try:
        # Step 1: Break down query
        sub_queries = await query_processor.breakdown_query(request.query)
        
        # Step 2: Parallel search across engines
        raw_results = await search_orchestrator.search_all(
            query=request.query,
            sub_queries=sub_queries,
            timeout=settings.search_timeout
        )
        
        # Step 3: Synthesize results
        synthesized = await result_synthesizer.synthesize(
            query=request.query,
            raw_results=raw_results,
            max_results=request.max_results
        )
        
        processing_time = asyncio.get_event_loop().time() - start_time
        
        return SearchResponse(
            query=request.query,
            sub_queries=sub_queries,
            results=synthesized["results"],
            summary=synthesized["summary"],
            engine_stats=synthesized["engine_stats"],
            processing_time=round(processing_time, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")


# WebSocket connection manager
class ConnectionManager:
    """Manages WebSocket connections for real-time updates."""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass


manager = ConnectionManager()


@app.websocket("/ws/process")
async def websocket_process(websocket: WebSocket):
    """
    WebSocket endpoint for real-time intelligent search.
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Wait for search request
            data = await websocket.receive_json()
            query = data.get("query", "")
            
            if not query:
                continue
            
            # Send process updates
            await websocket.send_json({
                "type": "status",
                "stage": "breaking_query",
                "message": "AI is analyzing your query..."
            })
            
            # Step 1: Query breakdown
            sub_queries = await query_processor.breakdown_query(query)
            await websocket.send_json({
                "type": "breakdown",
                "sub_queries": sub_queries,
                "message": f"Generated {len(sub_queries)} focused searches"
            })
            
            # Step 2: Search across engines
            await websocket.send_json({
                "type": "status",
                "stage": "searching",
                "message": "Searching across 5 engines..."
            })
            
            # Start parallel searches with progress updates
            async def search_with_updates():
                results = []
                async for engine_name, engine_results in search_orchestrator.search_all_streaming(query, sub_queries):
                    await websocket.send_json({
                        "type": "engine_complete",
                        "engine": engine_name,
                        "count": len(engine_results)
                    })
                    results.append((engine_name, engine_results))
                return dict(results)
            
            raw_results = await search_with_updates()
            
            # Step 3: Synthesis
            await websocket.send_json({
                "type": "status",
                "stage": "synthesizing",
                "message": "AI is synthesizing results..."
            })
            
            synthesized = await result_synthesizer.synthesize(query, raw_results, max_results=15)
            
            # Send final results
            await websocket.send_json({
                "type": "complete",
                "results": synthesized["results"],
                "summary": synthesized["summary"],
                "engine_stats": synthesized["engine_stats"]
            })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WS Error: {e}")
        import traceback
        traceback.print_exc()
        await websocket.send_json({
            "type": "error",
            "message": str(e)
        })
        manager.disconnect(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.backend_port,
        reload=True
    )
