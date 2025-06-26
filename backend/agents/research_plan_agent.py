# research_agent.py
import asyncio
from typing import Dict, Any, List
from base_agent import BaseAgent

# WebSearchEngine import düzeltmesi
try:
    from .web_search_engine import WebSearchEngine
except ImportError:
    print("⚠️ WebSearchEngine import edilemedi. Fallback arama kullanılacak.")
    WebSearchEngine = None


class ResearchAgent(BaseAgent):
    """
    Araştırma Agent'ı - Tek sorumluluğu web araması yapmak ve ham sonuçları döndürmek
    """
    
    def __init__(self, web_search_engine=None):
        super().__init__()
        if web_search_engine:
            self.search_engine = web_search_engine
        elif WebSearchEngine:
            self.search_engine = WebSearchEngine()
        else:
            self.search_engine = None
            print("⚠️ WebSearchEngine kullanılamıyor. Fallback veriler kullanılacak.")

        # DÜZELTME: İstatistikleri takip etmek için bir sözlük eklendi.
        self.stats = {
            'total_queries_executed': 0,
            'total_results_found': 0,
        }

    # DÜZELTME: İstatistikleri döndüren bir fonksiyon eklendi.
    def get_stats(self) -> Dict[str, int]:
        """Araştırma agent'ının istatistiklerini döndürür."""
        return self.stats.copy()

    def reset_stats(self):
        """İstatistikleri sıfırlar."""
        self.stats = {'total_queries_executed': 0, 'total_results_found': 0}

    async def search_for_data(self, query: str) -> List[Dict[str, Any]]:
        """Tek bir sorgu için web araması yapar ve istatistikleri günceller."""
        if not self.search_engine:
            print(f"⚠️ [Research] Search engine not available for query: {query}")
            return []
        
        try:
            # İstatistik güncellemesi
            self.stats['total_queries_executed'] += 1
            search_response = await self.search_engine.search(query=query)
            results = search_response.get("results", [])
            self.stats['total_results_found'] += len(results)
            print(f"✅ [Research] Found {len(results)} results for: {query}")
            return results
        except Exception as e:
            print(f"❌ [Research] Search call failed for '{query}': {e}")
            return []

    def generate_search_queries(self, idea_title: str, trends: List[str], metric_types: List[str]) -> Dict[str, List[str]]:
        """SaaS fikri ve metrik türlerine göre arama sorguları üretir."""
        main_topic = trends[0] if trends else idea_title.split()[0]
        query_templates = {
            'market_size': [f"{main_topic} software market size 2024", f"B2B {main_topic} market value"],
            'acv': [f"SaaS annual contract value {main_topic}", f"enterprise software annual revenue per customer"],
            'cac': [f"SaaS customer acquisition cost 2024", f"B2B software marketing cost per customer"],
            'churn': [f"SaaS churn rate benchmark 2024", f"B2B software customer retention"]
        }
        
        generated_queries = {m_type: query_templates.get(m_type, []) for m_type in metric_types}
        total_queries = sum(len(q) for q in generated_queries.values())
        print(f"🔍 [Research] Generated {total_queries} queries for {len(metric_types)} metric types")
        return generated_queries

    async def research_financial_metrics(self, idea_title: str, trends: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Finansal metrikler için kapsamlı araştırma yapar."""
        print(f"🌍 [Research] Starting comprehensive research for: {idea_title}")
        self.reset_stats() # Her yeni araştırma başında istatistikleri sıfırla
        
        metric_types = ['market_size', 'acv', 'cac', 'churn']
        query_groups = self.generate_search_queries(idea_title, trends, metric_types)
        
        all_results = {}
        for metric_type, queries in query_groups.items():
            print(f"🔍 [Research] Searching for {metric_type} data...")
            metric_results = []
            for query in queries:
                try:
                    results = await self.search_for_data(query)
                    metric_results.extend(results)
                    await asyncio.sleep(0.2)  # Rate limiting
                except Exception as e:
                    print(f"⚠️ [Research] Query failed: {e}")
            all_results[metric_type] = metric_results
        
        print(f"✅ [Research] Research complete. Stats: {self.get_stats()}")
        return all_results