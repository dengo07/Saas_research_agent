
from typing import List, Dict
from pydantic import ValidationError

# Kendi oluşturduğumuz modülleri import ediyoruz
from models import SaaSIdea

class ValidatorAgent:
    """Fikirleri doğrulayan, zenginleştiren ve veri bütünlüğünü sağlayan agent."""
    def validate_and_enrich_ideas(self, ideas_data: List[dict], original_research: dict, query: str) -> List[SaaSIdea]:
        print("🛡️ [Validator] Validating and enriching generated ideas...")
        validated_ideas = []
        for idea_data in ideas_data:
            try:
                # Eksik verileri orijinal araştırmadan tamamla
                idea_data.setdefault("competitors", original_research.get("competitors", []))
                idea_data.setdefault("trends", original_research.get("trends", []))
                idea_data.setdefault("reddit_insights", original_research.get("reddit_insights", ""))
                
                # Pydantic ile doğrulama
                validated_idea = SaaSIdea(**idea_data)
                validated_ideas.append(validated_idea)
            except ValidationError as e:
                print(f"⚠️ [Validator] Validation error for an idea: {e}")
                continue
        
        if not validated_ideas:
            print("⚠️ [Validator] No valid ideas from Analyzer. Creating a fallback idea.")
            fallback_idea = SaaSIdea(
                title=f"{query.title()} Management Platform",
                description=f"Comprehensive solution for managing {query} workflows.",
                source="Fallback Generation",
                potential=7,
                tags=[query.lower(), "management", "automation"],
                validation="Market research indicates a general demand for such tools.",
                marketSize="$500M+ potential market",
                painPoints=["Manual processes", "Lack of integration", "Poor visibility"],
                competitors=original_research.get("competitors", ["Generic SaaS"]),
                trends=original_research.get("trends", ["Digital transformation"]),
                reddit_insights=original_research.get("reddit_insights")
            )
            validated_ideas.append(fallback_idea)
            
        return validated_ideas
