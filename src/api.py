"""
FastAPI backend for the Business Info Retrieval Agent
Provides REST API endpoints for querying businesses
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
import os
import sys

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import agent system components
from agent_system import ReActAgent, AgentConfig
from language_model import LLM
from knowledge_base import TOOLS, CORPUS, search_corpus

app = FastAPI(title="Business Info Retrieval Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agent (lazy loading)
_agent = None

def get_agent():
    """Lazy initialization of the agent"""
    global _agent
    if _agent is None:
        _agent = ReActAgent(LLM, TOOLS, AgentConfig(max_steps=6, verbose=False))
    return _agent

# Request/Response models
class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5

class BusinessResult(BaseModel):
    business_id: str
    name: str
    address: str
    stars: float
    categories: List[str]
    similarity_score: float
    summary: str

class QueryResponse(BaseModel):
    reasoning: Optional[List[str]] = None
    retrieved: List[BusinessResult]

def extract_businesses_from_observations(steps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Extract unique businesses from agent observations"""
    businesses = {}
    for step in steps:
        try:
            obs = json.loads(step.get("observation", "{}"))
            if isinstance(obs, dict) and "results" in obs:
                for result in obs["results"]:
                    biz_id = result.get("id")
                    if biz_id and biz_id not in businesses:
                        businesses[biz_id] = {
                            "id": biz_id,
                            "title": result.get("title", ""),
                            "address": result.get("address", ""),
                            "city": result.get("city", ""),
                            "state": result.get("state", ""),
                            "stars": result.get("stars", 0.0),
                            "categories": result.get("categories", []),
                            "score": result.get("score", 0.0),
                            "snippet": result.get("snippet", "")
                        }
        except (json.JSONDecodeError, KeyError):
            continue
    return list(businesses.values())

def generate_summary(business: Dict[str, Any], query: str) -> str:
    """Generate a summary for a business using LLM"""
    try:
        # Simple summary based on available data
        name = business.get("title", "Unknown")
        stars = business.get("stars", 0.0)
        categories = business.get("categories", [])
        snippet = business.get("snippet", "")
        
        cat_str = ", ".join(categories[:3]) if categories else "business"
        summary = f"{name} is a {cat_str} with a {stars:.1f}-star rating. {snippet[:100]}..."
        return summary
    except Exception as e:
        return f"Business information available."

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.post("/api/query", response_model=QueryResponse)
async def query_businesses(request: QueryRequest):
    """
    Query businesses using the IR agent system
    """
    try:
        # Get agent and run query
        agent = get_agent()
        result = agent.run(request.query)
        
        # Extract reasoning steps
        reasoning = [step.get("thought", "") for step in result.get("steps", []) if step.get("thought")]
        
        # Extract businesses from observations
        businesses = extract_businesses_from_observations(result.get("steps", []))
        
        # If no businesses found in observations, do a direct search
        if not businesses:
            # Perform direct search as fallback
            search_results = search_corpus(request.query, k=request.top_k)
            businesses = []
            for hit in search_results:
                # Get full business data from CORPUS
                biz_id = hit.get("id")
                for biz in CORPUS:
                    if biz.get("id") == biz_id:
                        businesses.append({
                            "id": biz.get("id", ""),
                            "title": biz.get("title", ""),
                            "address": biz.get("address", ""),
                            "city": biz.get("city", ""),
                            "state": biz.get("state", ""),
                            "stars": biz.get("stars", 0.0),
                            "categories": biz.get("categories", []),
                            "score": hit.get("score", 0.0),
                            "snippet": biz.get("text", "")[:240]
                        })
                        break
        
        # Limit to top_k
        businesses = sorted(businesses, key=lambda x: x.get("score", 0.0), reverse=True)[:request.top_k]
        
        # Convert to BusinessResult format
        business_results = []
        for biz in businesses:
            # Handle categories - can be list, string, or None
            categories = biz.get("categories", [])
            if categories is None:
                categories = []
            elif isinstance(categories, str):
                # Handle comma-separated string or other formats
                if "," in categories:
                    categories = [c.strip() for c in categories.split(",") if c.strip()]
                elif categories.strip():
                    categories = [categories.strip()]
                else:
                    categories = []
            elif not isinstance(categories, list):
                categories = []
            
            # Handle address - can be string or None
            address = biz.get("address", "")
            if address is None:
                address = ""
            elif not isinstance(address, str):
                address = str(address)
            
            # Build full address if city/state available
            city = biz.get("city", "")
            state = biz.get("state", "")
            if city and state and address:
                address = f"{address}, {city}, {state}"
            elif city and address:
                address = f"{address}, {city}"
            
            business_results.append(BusinessResult(
                business_id=biz.get("id", ""),
                name=biz.get("title", "Unknown"),
                address=address,
                stars=float(biz.get("stars", 0.0)),
                categories=categories,
                similarity_score=float(biz.get("score", 0.0)),
                summary=generate_summary(biz, request.query)
            ))
        
        return QueryResponse(
            reasoning=reasoning if reasoning else None,
            retrieved=business_results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

