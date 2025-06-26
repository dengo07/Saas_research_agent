# researcher_agent.py
import os
import httpx
import re
import asyncio
from bs4 import BeautifulSoup
from typing import Dict, Any, List, Optional
from enum import Enum

from .web_search_engine import WebSearchEngine

class ResearcherAgent:
    """Web'den ham veri toplamakla görevli agent."""
    
    def __init__(self):
        self.search_engine = WebSearchEngine()
        self._cache = {}  # Basit in-memory cache
        
    async def search_web(self, query: str, use_cache: bool = True) -> Dict[str, Any]:
        """Genel web araması."""
        print(f"🔍 [Researcher] Searching web for: {query}")
        
        # Cache kontrolü
        if use_cache and query in self._cache:
            print(f"💾 [Researcher] Using cached result for: {query}")
            return self._cache[query]
        
        result = await self.search_engine.search(query)
        
        # Başarılı sonuçları cache'le
        if result.get("results"):
            self._cache[query] = result
        
        return result

    async def search_for_trends(self, query: str) -> List[str]:
        """Market trend araması."""
        print(f"📈 [Researcher] Searching for trends related to: {query}")
        
        # Query'den anahtar kelimeleri çıkar
        keywords = self._extract_keywords_from_query(query)
        
        # Akıllı trend sorguları
        trend_queries = []
        
        if keywords:
            main_keyword = keywords[0]
            trend_queries.extend([
                f"{main_keyword} market trends 2024 2025",
                f"{main_keyword} industry growth",
                f"{main_keyword} future predictions"
            ])
            
            # Category-based trends
            category = self._detect_category(query, keywords)
            if category:
                trend_queries.extend([
                    f"{category} market trends 2024",
                    f"{category} industry analysis"
                ])
        else:
            # Fallback
            short_query = self._shorten_query(query)
            trend_queries = [
                f"{short_query} trends 2024",
                f"{short_query} market analysis"
            ]
        
        all_trends = []
        
        for trend_query in trend_queries:
            try:
                trends_data = await self.search_engine.search(trend_query)
                snippets = [
                    r.get("snippet", "") 
                    for r in trends_data.get("results", [])[:3]
                    if r.get("snippet")
                ]
                all_trends.extend(snippets)
            except Exception as e:
                print(f"⚠️ Trend search failed for '{trend_query}': {e}")
                continue
        
        # Duplicateları temizle ve sınırla
        unique_trends = list(dict.fromkeys(all_trends))[:10]
        print(f"✅ [Researcher] Found {len(unique_trends)} trend insights")
        
        return unique_trends

    async def find_competitors(self, query: str) -> List[str]:
        """Competitor araması."""
        print(f"⚔️ [Researcher] Finding competitors for: {query}")
        
        # Query'den anahtar kelimeleri çıkar
        keywords = self._extract_keywords_from_query(query)
        
        # Akıllı competitor search queries
        competitor_queries = []
        
        if keywords:
            # Anahtar kelimelerle arama
            main_keyword = keywords[0]
            competitor_queries.extend([
                f"{main_keyword} competitors alternatives",
                f"{main_keyword} similar tools",
                f"best {main_keyword} software",
                f"{main_keyword} vs"
            ])
            
            # İkincil kelimelerle de ara
            if len(keywords) > 1:
                secondary = keywords[1]
                competitor_queries.extend([
                    f"{main_keyword} {secondary} alternatives",
                    f"{secondary} tools comparison"
                ])
        else:
            # Fallback: orijinal query'i kısalt
            short_query = self._shorten_query(query)
            competitor_queries = [
                f"{short_query} competitors",
                f"{short_query} alternatives",
                f"similar to {short_query}"
            ]
        
        competitors = set()
        
        for comp_query in competitor_queries:
            try:
                comp_data = await self.search_engine.search(comp_query)
                
                for result in comp_data.get("results", [])[:5]:
                    text = f"{result.get('title', '')} {result.get('snippet', '')}"
                    
                    # İyileştirilmiş competitor extraction
                    # Büyük harfle başlayan kelimeler (brand names)
                    potential_names = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
                    
                    # URL'lerden domain isimleri
                    urls = re.findall(r'https?://(?:www\.)?([a-zA-Z0-9-]+)\.', text)
                    
                    for name in potential_names + urls:
                        if len(name) > 3 and name.lower() not in ['this', 'that', 'with', 'from', 'your']:
                            competitors.add(name)
                            
            except Exception as e:
                print(f"⚠️ Competitor search failed for '{comp_query}': {e}")
                continue
        
        competitor_list = list(competitors)[:15]
        print(f"✅ [Researcher] Found {len(competitor_list)} potential competitors")
        
        return competitor_list

    async def get_reddit_insights(self, query: str) -> str:
        """Reddit'ten insight toplama."""
        print(f"💬 [Researcher] Getting Reddit insights for: {query}")
        
        # Query'den anahtar kelimeleri çıkar
        keywords = self._extract_keywords_from_query(query)
        
        # Akıllı Reddit searches
        reddit_queries = []
        
        if keywords:
            main_keyword = keywords[0]
            reddit_queries.extend([
                f"site:reddit.com {main_keyword} problems",
                f"site:reddit.com {main_keyword} frustrating",
                f"site:reddit.com {main_keyword} wish",
                f"site:reddit.com {main_keyword} pain points"
            ])
            
            # İkincil kelimelerle pain point arama
            if len(keywords) > 1:
                secondary = keywords[1]
                reddit_queries.extend([
                    f"site:reddit.com {main_keyword} {secondary} issues",
                    f"site:reddit.com need better {secondary}"
                ])
        else:
            # Fallback
            short_query = self._shorten_query(query)
            reddit_queries = [
                f"site:reddit.com {short_query} problems",
                f"site:reddit.com {short_query} issues"
            ]
        
        all_insights = []
        
        for reddit_query in reddit_queries:
            try:
                reddit_data = await self.search_engine.search(reddit_query)
                insights = [
                    r.get("snippet", "") 
                    for r in reddit_data.get("results", [])[:2]
                    if r.get("snippet")
                ]
                all_insights.extend(insights)
                
            except Exception as e:
                print(f"⚠️ Reddit search failed for '{reddit_query}': {e}")
                continue
        
        if all_insights:
            # Insights'ları temizle ve birleştir
            cleaned_insights = [
                insight.strip() 
                for insight in all_insights 
                if len(insight.strip()) > 20
            ]
            
            result = " | ".join(cleaned_insights[:5])
            print(f"✅ [Researcher] Found {len(cleaned_insights)} Reddit insights")
            return result
        else:
            print("⚠️ [Researcher] No Reddit insights found")
            return "No specific Reddit insights found."
    
    def _extract_keywords_from_query(self, query: str) -> List[str]:
        """Query'den en önemli anahtar kelimeleri çıkarır."""
        # Stop words listesi
        stop_words = {
            'for', 'students', 'that', 'helps', 'with', 'and', 'or', 'the', 'a', 'an', 
            'to', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'will', 'would',
            'can', 'could', 'should', 'may', 'might', 'must', 'shall', 'in', 'on',
            'at', 'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'among', 'this', 'these', 'those',
            'platform', 'tool', 'application', 'app', 'software', 'system', 'service'
        }
        
        # Query'i temizle ve kelimelere ayır
        import re
        words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
        
        # Stop words'leri filtrele
        keywords = [word for word in words if word not in stop_words]
        
        # Frekansa göre sırala (basit scoring)
        word_scores = {}
        for word in keywords:
            # Önemli kelimeler için extra puan
            score = 1
            if any(term in word for term in ['manage', 'track', 'collaborat', 'social', 'learn']):
                score += 2
            if any(term in word for term in ['project', 'task', 'team', 'document']):
                score += 1
            
            word_scores[word] = word_scores.get(word, 0) + score
        
        # Score'a göre sırala
        sorted_keywords = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
        
        # En iyi 3-5 kelimeyi döndür
        result = [word for word, score in sorted_keywords[:5]]
        print(f"🔍 Extracted keywords from '{query}': {result}")
        return result
    
    def _detect_category(self, query: str, keywords: List[str]) -> str:
        """Query'den category/domain detect eder."""
        query_lower = query.lower()
        
        categories = {
            'education': ['student', 'learn', 'study', 'academic', 'school', 'university', 'course'],
            'productivity': ['task', 'project', 'manage', 'organize', 'track', 'workflow'],
            'collaboration': ['team', 'collaborate', 'share', 'group', 'social', 'peer'],
            'business': ['business', 'enterprise', 'company', 'corporate', 'sales'],
            'creative': ['design', 'creative', 'art', 'visual', 'brainstorm'],
            'communication': ['chat', 'message', 'video', 'meeting', 'communicate'],
            'analytics': ['data', 'analytics', 'report', 'dashboard', 'metric']
        }
        
        for category, terms in categories.items():
            if any(term in query_lower for term in terms):
                print(f"🎯 Detected category: {category}")
                return category
        
        return ""
    
    def _shorten_query(self, query: str) -> str:
        """Uzun query'leri kısaltır."""
        # İlk 3-4 kelimeyi al veya 50 karaktere kırp
        words = query.split()
        
        if len(words) <= 4:
            return query
        
        # İlk 4 kelimeyi al
        short = ' '.join(words[:4])
        
        # Eğer hala çok uzunsa, karaktere göre kırp
        if len(short) > 50:
            short = query[:47] + "..."
        
        print(f"✂️ Shortened query from '{query}' to '{short}'")
        return short
    
    async def comprehensive_research(self, query: str) -> Dict[str, Any]:
        """Comprehensive research for a given query."""
        print(f"🎯 [Researcher] Starting comprehensive research for: {query}")
        
        try:
            # Paralel olarak farklı araştırmaları yap
            tasks = [
                self.search_web(query),
                self.search_for_trends(query),
                self.find_competitors(query),
                self.get_reddit_insights(query)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Sonuçları organize et
            research_data = {
                "query": query,
                "general_search": results[0] if not isinstance(results[0], Exception) else {"results": [], "error": str(results[0])},
                "trends": results[1] if not isinstance(results[1], Exception) else [],
                "competitors": results[2] if not isinstance(results[2], Exception) else [],
                "reddit_insights": results[3] if not isinstance(results[3], Exception) else "No insights found",
                "timestamp": asyncio.get_event_loop().time()
            }
            
            print(f"✅ [Researcher] Comprehensive research completed for: {query}")
            return research_data
            
        except Exception as e:
            print(f"❌ [Researcher] Comprehensive research failed: {e}")
            return {
                "query": query,
                "error": str(e),
                "general_search": {"results": []},
                "trends": [],
                "competitors": [],
                "reddit_insights": "Research failed"
            }