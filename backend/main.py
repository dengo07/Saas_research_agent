# main.py
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List
import traceback
import time
import hashlib

# Kendi oluşturduğumuz modülleri import ediyoruz
from models import ResearchQuery, SaaSIdea, BusinessPlan, BusinessPlanRequest
from agents.master_agent import MasterAgent

# --- FastAPI UYGULAMA KURULUMU ---
app = FastAPI(
    title="SaaS Research Agent Backend",
    description="AI-powered SaaS research with real agent-based intelligence",
    version="4.0.0"
)

# CORS (Cross-Origin Resource Sharing) Ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:5500", "null"], # Gerekirse frontend adreslerinizi ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hata Yakalama (Exception Handling)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    print(f"❌ Global Error [{error_id}]: {str(exc)}")
    print(f"🔍 Traceback: {traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": str(exc), "error_id": error_id}
    )

# --- AGENT'I OLUŞTURMA ---
# Uygulama başlarken MasterAgent'ın bir örneğini oluşturuyoruz.
agent = MasterAgent()

# --- API ENDPOINTS ---
@app.get("/")
def read_root():
    return {"message": "SaaS Research Agent Backend'ine hoş geldiniz! (Multi-File)"}

@app.post("/api/research", response_model=List[SaaSIdea])
async def start_research(query: ResearchQuery):
    try:
        ideas = await agent.research_saas_ideas(query.query, config=query)
        if not ideas:
            raise HTTPException(status_code=404, detail="No SaaS ideas could be generated for the given query.")
        return ideas
    except Exception as e:
        print(f"❌ Error during research for query '{query.query}': {e}")
        raise e

@app.post("/api/business-plan", response_model=BusinessPlan)
async def create_business_plan(request: BusinessPlanRequest):
    try:
        plan = await agent.generate_business_plan(request.idea)
        return plan
    except Exception as e:
        print(f"❌ Error creating business plan for '{request.idea.title}': {e}")
        raise e
    
@app.get("/api/health", status_code=status.HTTP_200_OK)
def health_check():
    """Frontend'in backend'in çalışıp çalışmadığını kontrol etmesi için basit bir endpoint."""
    return {"status": "ok", "message": "Backend is running and healthy!"}

@app.get("/api/cache-stats")
def get_cache_stats():
    """
    Önbellek istatistiklerini döndürür.
    Not: Önbellekleme (caching) mantığı henüz yeni agent mimarisine
    tam olarak entegre edilmediği için bu endpoint şimdilik
    temsili veriler döndürmektedir.
    """
    return {
        "status": "caching_not_fully_implemented",
        "message": "Cache stats are not available in the current agent architecture.",
        "memory_cache_items": 0,
        "redis_status": "disconnected"
    }