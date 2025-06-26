# master_agent.py

import asyncio
import json
# Hatanın çözümü için 'List' tipini typing kütüphanesinden import ediyoruz.
from typing import List 

# Kendi oluşturduğumuz modülleri import ediyoruz
from models import ResearchQuery, SaaSIdea, BusinessPlan
from .researcher_agent import ResearcherAgent
from .analyzer_agent import AnalyzerAgent
from .validator_agent import ValidatorAgent
from .planner_agent import PlannerAgent
from .web_search_engine import WebSearchEngine

class MasterAgent:
    """Tüm agent'ları yöneten ve süreci baştan sona yürüten ana agent."""
    def __init__(self):
        self.researcher = ResearcherAgent()
        self.analyzer = AnalyzerAgent()
        self.validator = ValidatorAgent()
        self.planner = PlannerAgent()
        print("✅ MasterAgent and its team of specialized agents are ready.")

    async def research_saas_ideas(self, query: str, config: ResearchQuery) -> List[SaaSIdea]:
        """
        Agent ekibini kullanarak baştan sona bir SaaS fikri araştırma süreci yürütür.
        """
        print(f"🚀 [MasterAgent] Starting full research process for: {query}")
        
        # Adım 1: Araştırmacı Agent ile paralel veri toplama
        tasks = [
            self.researcher.search_web(f"{query} problems pain points"),
            self.researcher.search_web(f"{query} startup ideas opportunities")
        ]
        if config.include_trends:
            tasks.append(self.researcher.search_for_trends(query))
        if config.include_competitors:
            tasks.append(self.researcher.find_competitors(query))
        if config.include_reddit:
            tasks.append(self.researcher.get_reddit_insights(query))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Sonuçları işleyerek analizci için bir bağlam (context) oluşturma
        pain_points_data = results[0] if not isinstance(results[0], Exception) else {"results": []}
        opportunities_data = results[1] if not isinstance(results[1], Exception) else {"results": []}
        
        research_context = {
            "pain_points": [r.get('snippet', '') for r in pain_points_data.get('results', [])[:5]],
            "opportunities": [r.get('snippet', '') for r in opportunities_data.get('results', [])[:5]],
        }
        
        idx = 2
        if config.include_trends:
            research_context["trends"] = results[idx] if not isinstance(results[idx], Exception) else []
            idx += 1
        if config.include_competitors:
            research_context["competitors"] = results[idx] if not isinstance(results[idx], Exception) else []
            idx += 1
        if config.include_reddit:
            research_context["reddit_insights"] = results[idx] if not isinstance(results[idx], Exception) else ""

        # Adım 2: Analizci Agent ile fikir üretme
        generated_ideas = await self.analyzer.generate_saas_ideas(query, json.dumps(research_context, indent=2))
        
        # Adım 3: Doğrulayıcı Agent ile fikirleri doğrulama ve zenginleştirme
        final_ideas = self.validator.validate_and_enrich_ideas(generated_ideas, research_context, query)
        
        print(f"✅ [MasterAgent] Research completed. Found {len(final_ideas)} validated ideas.")
        return final_ideas

    async def generate_business_plan(self, idea: SaaSIdea) -> BusinessPlan:
        """İş planı oluşturma görevini doğrudan PlannerAgent'a devreder."""
        return await self.planner.generate_business_plan(idea)
