import os
import httpx
import re
import asyncio
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
from enum import Enum
from dotenv import load_dotenv
load_dotenv()

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
SERPER_API_KEY = os.getenv("SERPAPI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

class SearchProvider(Enum):
    SERPAPI = "serpapi"
    SERPER = "serper"
    TAVILY = "tavily"
    DUCKDUCKGO = "duckduckgo"

class WebSearchEngine:
    
    def __init__(self):
        self.serpapi_key = SERPAPI_API_KEY
        self.serper_key = SERPER_API_KEY
        self.tavily_key = TAVILY_API_KEY
        self.timeout = 30  # Request timeout
        
    async def search(self, query: str, provider: SearchProvider = None) -> Dict[str, Any]:
        """Ana search metodu - provider'ları priority sırasıyla dener."""
        providers = self._get_available_providers(provider)
        
        for p in providers:
            try:
                print(f"🔍 Trying {p.value} for query: {query}")
                result = await self._execute_search(p, query)
                if result and result.get("results"):
                    print(f"✅ {p.value} search successful - {len(result['results'])} results")
                    return result
                else:
                    print(f"⚠️ {p.value} returned empty results")
            except Exception as e:
                print(f"❌ {p.value} search failed: {str(e)}")
                continue
        
        print("❌ All search providers failed")
        return {"results": [], "source": "none", "error": "All search providers failed"}
    
    def _get_available_providers(self, provider: Optional[SearchProvider]) -> List[SearchProvider]:
        """Kullanılabilir provider'ları priority sırasına göre döner."""
        if provider:
            return [provider]
        
        providers = []
        # API key'i olan provider'ları öncelikle ekle
        if self.tavily_key: 
            providers.append(SearchProvider.TAVILY)
        if self.serper_key: 
            providers.append(SearchProvider.SERPER)
        if self.serpapi_key: 
            providers.append(SearchProvider.SERPAPI)
        
        # DuckDuckGo'yu fallback olarak ekle
        providers.append(SearchProvider.DUCKDUCKGO)
        return providers
    
    async def _execute_search(self, provider: SearchProvider, query: str) -> Dict[str, Any]:
        """Belirli bir provider ile search yapar."""
        search_methods = {
            SearchProvider.TAVILY: self._search_tavily,
            SearchProvider.SERPER: self._search_serper,
            SearchProvider.SERPAPI: self._search_serpapi,
            SearchProvider.DUCKDUCKGO: self._search_duckduckgo
        }
        
        method = search_methods.get(provider)
        if not method:
            raise ValueError(f"Unsupported provider: {provider}")
        
        return await method(query)
    
    async def _search_tavily(self, query: str) -> Dict[str, Any]:
        """Tavily API ile arama."""
        if not self.tavily_key:
            raise ValueError("Tavily API key not configured")
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://api.tavily.com/search",
                json={
                    "api_key": self.tavily_key,
                    "query": query,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "include_raw_content": False,
                    "max_results": 10
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "results": [
                    {
                        "title": r.get("title", ""),
                        "snippet": r.get("content", ""),
                        "link": r.get("url", ""),
                        "score": r.get("score", 0)
                    } 
                    for r in data.get("results", [])
                ],
                "answer": data.get("answer", ""),
                "source": "tavily"
            }
        
    async def _search_serper(self, query: str) -> Dict[str, Any]:
        """Serper API ile arama."""
        if not self.serper_key:
            raise ValueError("Serper API key not configured")
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": self.serper_key,
                    "Content-Type": "application/json"
                },
                json={"q": query, "num": 10}
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "results": [
                    {
                        "title": r.get("title", ""),
                        "snippet": r.get("snippet", ""),
                        "link": r.get("link", "")
                    } 
                    for r in data.get("organic", [])
                ],
                "relatedSearches": [
                    r.get("query", "") for r in data.get("relatedSearches", [])
                ],
                "source": "serper"
            }
        
    async def _search_serpapi(self, query: str) -> Dict[str, Any]:
        """SerpAPI ile arama."""
        if not self.serpapi_key:
            raise ValueError("SerpAPI key not configured")
            
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                "https://serpapi.com/search",
                params={
                    "api_key": self.serpapi_key,
                    "q": query,
                    "engine": "google",
                    "num": 10
                }
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "results": [
                    {
                        "title": r.get("title", ""),
                        "snippet": r.get("snippet", ""),
                        "link": r.get("link", "")
                    } 
                    for r in data.get("organic_results", [])
                ],
                "source": "serpapi"
            }
        
    async def _search_duckduckgo(self, query: str) -> Dict[str, Any]:
        """DuckDuckGo ile arama."""
        try:
            from duckduckgo_search import AsyncDDGS
            
            async with AsyncDDGS() as ddgs:
                # Rate limiting için biraz bekle
                await asyncio.sleep(1)
                
                results = await ddgs.text(query, max_results=10)
                
                return {
                    "results": [
                        {
                            "title": r.get("title", ""),
                            "snippet": r.get("body", ""),
                            "link": r.get("href", "")
                        } 
                        for r in results if r  # None check
                    ],
                    "source": "duckduckgo"
                }
        except ImportError:
            print("⚠️ duckduckgo_search package not installed")
            return await self._search_fallback(query)
        except Exception as e:
            print(f"⚠️ DuckDuckGo search error: {e}")
            return await self._search_fallback(query)
        
    async def _search_fallback(self, query: str) -> Dict[str, Any]:
        """Fallback search method."""
        print("⚠️ Using fallback search method")
        # Basit bir fallback implementasyonu
        return {
            "results": [
                {
                    "title": f"Search for: {query}",
                    "snippet": "Fallback search method used - limited results available",
                    "link": ""
                }
            ], 
            "source": "fallback"
        }
