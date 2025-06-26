# business_plan_writer_agent.py
import json
import re
from typing import Dict, Any, Optional, List
from base_agent import BaseAgent
from models import SaaSIdea

class BusinessPlanWriterAgent(BaseAgent):
    """
    İş Planı Yazma Agent'ı - LLM'i kullanarak anlatısal iş planı içerikleri üretir,
    bu içerikleri doğrular ve finansal analizlerle zenginleştirir.
    """

    def __init__(self):
        super().__init__()
        self.generation_stats = {
            'plans_generated': 0, 'llm_calls_made': 0,
            'json_parse_successes': 0, 'json_parse_failures': 0,
            'fallback_plans_created': 0
        }

    async def generate_business_plan_content(
        self, idea: SaaSIdea, financial_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ana iş planı içerik üretme fonksiyonu. LLM'i çağırır, yanıtı parse eder
        veya başarısız olursa bir fallback oluşturur.
        """
        print(f"✍️ [WriterAgent] Generating content for: {idea.title}")
        try:
            prompt = self._create_structured_prompt(idea, financial_analysis)
            system_prompt = self._create_structured_system_prompt()

            llm_response = await self.call_llm(prompt, system_prompt)
            self.generation_stats['llm_calls_made'] += 1
            print(f"🤖 [WriterAgent] LLM response received: {len(llm_response)} characters")

            parsed_content = self._parse_structured_response(llm_response)

            if parsed_content:
                self.generation_stats['json_parse_successes'] += 1
                print("✅ [WriterAgent] Successfully parsed structured LLM response")
                return parsed_content
            else:
                print("⚠️ [WriterAgent] Structured parse failed, creating intelligent fallback.")
                self.generation_stats['json_parse_failures'] += 1
                return self._create_structured_fallback_content(idea, financial_analysis)

        except Exception as e:
            print(f"❌ [WriterAgent] Critical error during content generation: {e}")
            self.generation_stats['json_parse_failures'] += 1
            return self._create_structured_fallback_content(idea, financial_analysis)

    def create_competitive_analysis(self, idea: SaaSIdea, financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Competitive Advantage Matrix için gerekli verileri oluşturur."""
        competitor_count = len(idea.competitors) if idea.competitors else 0
        pain_point_count = len(idea.painPoints) if idea.painPoints else 1
        market_size = financial_analysis.get('financial_metrics', {}).get('market_size', 100000000)
        
        # Market difficulty hesapla
        if competitor_count > 10:
            difficulty = 0.8
            position = 'challenging'
        elif competitor_count > 5:
            difficulty = 0.6
            position = 'competitive'
        else:
            difficulty = 0.3
            position = 'emerging'
        
        # Competitive scores hesapla
        base_score = 70
        innovation_boost = pain_point_count * 5
        difficulty_penalty = int(difficulty * 20)
        
        scores = {
            'innovation': max(50, min(100, base_score + innovation_boost - difficulty_penalty)),
            'quality': max(60, min(100, base_score + 5 - difficulty_penalty)),
            'pricing': max(55, min(100, base_score - 5 - difficulty_penalty))
        }
        
        # Frontend için radar chart verisi - frontend'in beklediği format
        radar_data = {
            'labels': ['Price', 'Features', 'Quality', 'Marketing', 'Innovation'],
            'yourBusiness': [
                scores['pricing'],           # Price
                scores['innovation'] - 5,    # Features  
                scores['quality'],           # Quality
                max(50, base_score - 10),    # Marketing
                scores['innovation']         # Innovation
            ],
            'competitorAvg': [
                70,  # Price - competitor average
                75,  # Features
                80,  # Quality
                85,  # Marketing
                70   # Innovation
            ]
        }
        
        return {
            'market_position': position,
            'differentiation_score': max(60, 100 - int(difficulty * 40)),
            'pain_points_addressed': pain_point_count,
            'competitive_intensity': difficulty,
            'scores': scores,
            'advantages': [
                f"Superior user experience compared to {idea.competitors[0] if idea.competitors else 'existing solutions'}",
                f"Focused solution for {idea.painPoints[0] if idea.painPoints else 'specific market needs'}",
                "Modern technology stack and faster implementation"
            ],
            # Frontend'in beklediği format - matrix_data yerine radar chart data
            'labels': radar_data['labels'],
            'yourBusiness': radar_data['yourBusiness'], 
            'competitorAvg': radar_data['competitorAvg']
        }

    def validate_and_enhance_content(
        self, content: Dict[str, Any], idea: SaaSIdea, financial_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Üretilen içeriği doğrular, eksik alanları tamamlar ve ek analitik bölümler ekler.
        """
        print("🔧 [WriterAgent] Validating and enhancing plan content...")
        enhanced_content = content.copy()
        required_fields = [
            'targetAudience', 'coreFeatures', 'monetizationModel', 'marketingStrategy',
            'competitiveAdvantage', 'researchInsights', 'painPointsAddressed',
            'marketOpportunity', 'riskAnalysis'
        ]
        
        for field in required_fields:
            if field not in enhanced_content or not enhanced_content[field]:
                print(f"⚠️ [WriterAgent] Enhancing missing content for '{field}'")
                enhanced_content[field] = self._get_structured_template_for_field(field, idea, financial_analysis)
            elif isinstance(enhanced_content[field], str) and len(enhanced_content[field]) < 100:
                print(f"⚠️ [WriterAgent] Enhancing insufficient content for '{field}'")
                enhanced_content[field] = self._get_structured_template_for_field(field, idea, financial_analysis)

        # Ek içerikler ekle
        enhanced_content['executiveSummary'] = self.generate_executive_summary(idea, financial_analysis, enhanced_content)
        enhanced_content['financialHighlights'] = self.create_financial_highlights(financial_analysis)
        enhanced_content['mvpRoadmap'] = self.create_mvp_roadmap_from_analysis(idea, financial_analysis)
        enhanced_content['competitiveAnalysis'] = self.create_competitive_analysis(idea, financial_analysis)
        
        self.generation_stats['plans_generated'] += 1
        print("✅ [WriterAgent] Content validation and enhancement completed.")
        return enhanced_content
    
    def _create_structured_system_prompt(self) -> str:
        return """You are an expert SaaS business strategist. You create comprehensive, data-driven business plans.

CRITICAL REQUIREMENTS:
1. You MUST return ONLY a valid JSON object
2. Each field must be a structured object, NOT a string
3. Follow the exact schema provided in the user prompt
4. No additional text, explanations, or markdown - ONLY JSON
5. Ensure all nested objects have meaningful keys and values

Your responses must be detailed, specific, and data-driven."""

    def _create_structured_prompt(self, idea: SaaSIdea, financial_analysis: Dict[str, Any]) -> str:
        metrics = financial_analysis.get('financial_metrics', {})
        market_size = metrics.get('market_size', 250_000_000)
        acv = metrics.get('acv', 8000)
        cac = metrics.get('cac', 2500)
        financial_instruction = ""
        if market_size == 250_000_000 or acv == 8000 or cac == 2500:
            financial_instruction = """
        CRITICAL FINANCIAL TASK: The financial data provided below contains default placeholder values.
        Your first task is to RESEARCH and REPLACE these default values with realistic, data-driven estimates for this specific business idea.
        You MUST use your researched values in the business plan.
        Default Values to be Replaced: TAM=${market_size:,.0f}, ACV=${acv:,.0f}, CAC=${cac:,.0f}.
    """
        else:
            financial_instruction = f"""
        FINANCIAL CONTEXT: Use the following pre-validated financial data in your plan.
        TAM is ${market_size:,.0f}, Target ACV is ${acv:,.0f}, Target CAC is ${cac:,.0f}.
        """
        return f"""
    Create a comprehensive business plan for the SaaS idea: '{idea.title}' ({idea.description}).

    {financial_instruction}

    After determining the correct financial metrics, generate ONLY a valid JSON object with the EXACT structure below. Do not include any other text or explanations.

{{
  "targetAudience": {{
    "primary": "detailed primary audience description",
    "secondary": "secondary audience if applicable", 
    "demographics": "age, company size, role, industry",
    "painPoints": ["main pain point 1", "main pain point 2"],
    "buyingBehavior": "how they make purchasing decisions"
  }},
  "coreFeatures": {{
    "feature1": {{
      "name": "Feature Name",
      "description": "Detailed description",
      "value": "Business value provided"
    }},
    "feature2": {{
      "name": "Feature Name", 
      "description": "Detailed description",
      "value": "Business value provided"
    }},
    "feature3": {{
      "name": "Feature Name",
      "description": "Detailed description", 
      "value": "Business value provided"
    }}
  }},
  "monetizationModel": {{
    "type": "SaaS subscription/freemium/usage-based",
    "pricingTiers": {{
      "basic": {{"price": "monthly price", "features": ["feature1", "feature2"]}},
      "pro": {{"price": "monthly price", "features": ["feature1", "feature2", "feature3"]}},
      "enterprise": {{"price": "monthly price", "features": ["all features plus custom"]}}
    }},
    "revenueModel": "how revenue is generated",
    "pricingStrategy": "competitive positioning and rationale"
  }},
  "marketingStrategy": {{
    "channels": {{
      "digital": ["SEO", "content marketing", "social media"],
      "traditional": ["events", "partnerships", "PR"],
      "sales": ["inbound", "outbound", "channel partners"]
    }},
    "messaging": "core value proposition and positioning",
    "customerAcquisition": "detailed acquisition strategy",
    "retentionStrategy": "how to keep customers engaged"
  }},
  "competitiveAdvantage": {{
    "differentiators": ["unique advantage 1", "unique advantage 2", "unique advantage 3"],
    "barriers": "barriers to entry for competitors",
    "moat": "sustainable competitive advantages",
    "positioning": "how you position against competitors"
  }},
  "researchInsights": {{
    "marketTrends": ["trend 1", "trend 2", "trend 3"],
    "customerNeeds": "unmet needs in the market",
    "opportunitySize": "size and growth of opportunity",
    "validationEvidence": "evidence supporting market demand"
  }},
  "painPointsAddressed": {{
    "primary": {{"problem": "main problem", "solution": "how you solve it", "impact": "business impact"}},
    "secondary": {{"problem": "secondary problem", "solution": "how you solve it", "impact": "business impact"}},
    "tertiary": {{"problem": "third problem", "solution": "how you solve it", "impact": "business impact"}}
  }},
  "marketOpportunity": {{
    "totalMarket": "TAM description and size",
    "serviceableMarket": "SAM description and size", 
    "targetMarket": "SOM description and size",
    "growthDrivers": ["driver 1", "driver 2", "driver 3"],
    "marketDynamics": "how the market is evolving"
  }},
  "riskAnalysis": {{
    "marketRisks": ["risk 1", "risk 2"],
    "competitiveRisks": ["risk 1", "risk 2"],
    "technicalRisks": ["risk 1", "risk 2"],
    "mitigationStrategies": {{
      "market": "how to mitigate market risks",
      "competitive": "how to mitigate competitive risks", 
      "technical": "how to mitigate technical risks"
    }}
  }}
}}

IMPORTANT: Return ONLY the JSON object above. No additional text, explanations, or formatting.
        """

    def _parse_structured_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Structured JSON response'u parse eder."""
        if not response or not response.strip():
            return None
            
        # JSON'u bul ve parse et
        try:
            # Sadece JSON kısmını al
            response = response.strip()
            if response.startswith('```json'):
                response = response.replace('```json', '').replace('```', '').strip()
            elif response.startswith('```'):
                response = response.replace('```', '').strip()
                
            # JSON objesi bul
            start = response.find('{')
            end = response.rfind('}') + 1
            
            if start != -1 and end > start:
                json_str = response[start:end]
                parsed = json.loads(json_str)
                
                # Gerekli alanların structured olduğunu kontrol et
                required_fields = [
                    'targetAudience', 'coreFeatures', 'monetizationModel', 
                    'marketingStrategy', 'competitiveAdvantage', 'researchInsights',
                    'painPointsAddressed', 'marketOpportunity', 'riskAnalysis'
                ]
                
                # Her alanın dict olduğunu kontrol et
                valid_structure = True
                for field in required_fields:
                    if field in parsed and not isinstance(parsed[field], dict):
                        print(f"⚠️ Field '{field}' is not a dictionary: {type(parsed[field])}")
                        valid_structure = False
                        
                if valid_structure and len(parsed) >= 8:
                    return parsed
                    
        except json.JSONDecodeError as e:
            print(f"❌ JSON Parse Error: {e}")
        except Exception as e:
            print(f"❌ General Parse Error: {e}")
            
        return None

    def _create_structured_fallback_content(self, idea: SaaSIdea, financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Structured fallback content oluşturur."""
        print("🔄 [WriterAgent] Creating structured fallback content...")
        self.generation_stats['fallback_plans_created'] += 1
        
        return {
            field: self._get_structured_template_for_field(field, idea, financial_analysis) 
            for field in [
                'targetAudience', 'coreFeatures', 'monetizationModel', 'marketingStrategy',
                'competitiveAdvantage', 'researchInsights', 'painPointsAddressed',
                'marketOpportunity', 'riskAnalysis'
            ]
        }

    def _get_structured_template_for_field(self, field: str, idea: SaaSIdea, financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Structured template döndürür - her alan dictionary objesi olarak."""
        metrics = financial_analysis.get('financial_metrics', {})
        acv = metrics.get('acv', 8000)
        market_size = metrics.get('market_size', 250_000_000)
        main_trend = idea.trends[0] if idea.trends else 'technology'
        primary_pain_point = idea.painPoints[0] if idea.painPoints else 'operational inefficiency'
        competitor = idea.competitors[0] if idea.competitors else 'existing solutions'

        templates = {
            'targetAudience': {
                "primary": f"Mid-market companies (100-1000 employees) in the {main_trend} industry",
                "secondary": "Enterprise clients looking for specialized solutions",
                "demographics": "VPs and Directors, age 35-50, tech-savvy decision makers",
                "painPoints": [primary_pain_point, "lack of integration", "time-consuming processes"],
                "buyingBehavior": "Research-driven, require ROI demonstrations, prefer pilot programs"
            },
            
            'coreFeatures': {
                "feature1": {
                    "name": "AI-Powered Analytics",
                    "description": f"Advanced analytics engine that addresses {primary_pain_point}",
                    "value": "Reduces analysis time by 60% and improves decision accuracy"
                },
                "feature2": {
                    "name": "Customizable Dashboard",
                    "description": "User-friendly interface with drag-and-drop customization",
                    "value": "Improves user adoption and reduces training time"
                },
                "feature3": {
                    "name": "Seamless Integrations",
                    "description": "Pre-built connectors for popular business tools",
                    "value": "Eliminates data silos and improves workflow efficiency"
                }
            },
            
            'monetizationModel': {
                "type": "Tiered SaaS subscription",
                "pricingTiers": {
                    "basic": {"price": f"${int(acv/36):,}/month", "features": ["Core analytics", "Basic dashboard"]},
                    "pro": {"price": f"${int(acv/12):,}/month", "features": ["Advanced analytics", "Custom dashboard", "Integrations"]},
                    "enterprise": {"price": f"${int(acv*2/12):,}/month", "features": ["All features", "Custom development", "Priority support"]}
                },
                "revenueModel": "Recurring subscription revenue with annual discounts",
                "pricingStrategy": "Value-based pricing aligned with customer ROI"
            },
            
            'marketingStrategy': {
                "channels": {
                    "digital": ["SEO for industry keywords", "Content marketing", "LinkedIn advertising"],
                    "traditional": ["Industry conferences", "Partner channel", "Webinar series"],
                    "sales": ["Inbound lead qualification", "Outbound prospecting", "Channel partners"]
                },
                "messaging": f"The only {main_trend} solution that solves {primary_pain_point} in under 30 days",
                "customerAcquisition": "Content-driven inbound strategy with targeted outbound campaigns",
                "retentionStrategy": "Customer success program with quarterly business reviews"
            },
            
            'competitiveAdvantage': {
                "differentiators": [
                    f"Specialized focus on {main_trend} industry",
                    "Superior user experience and faster implementation",
                    "AI-driven insights not available in legacy solutions"
                ],
                "barriers": "Strong customer relationships and industry expertise",
                "moat": "Network effects and proprietary data algorithms",
                "positioning": f"The modern alternative to complex enterprise solutions like {competitor}"
            },
            
            'researchInsights': {
                "marketTrends": [
                    f"Growing demand for {main_trend} solutions",
                    "Shift toward AI-powered business tools",
                    "Increasing focus on user experience"
                ],
                "customerNeeds": f"Simple, effective solutions for {primary_pain_point}",
                "opportunitySize": f"${market_size:,} TAM with 15% annual growth",
                "validationEvidence": "Customer interviews and market research data"
            },
            
            'painPointsAddressed': {
                "primary": {
                    "problem": primary_pain_point,
                    "solution": "Automated workflows and AI-powered insights",
                    "impact": "60% reduction in manual effort and improved accuracy"
                },
                "secondary": {
                    "problem": "Lack of real-time visibility",
                    "solution": "Live dashboard with customizable metrics",
                    "impact": "Faster decision-making and improved team alignment"
                },
                "tertiary": {
                    "problem": "Complex integration requirements",
                    "solution": "Pre-built connectors and API framework",
                    "impact": "Reduced implementation time from months to weeks"
                }
            },
            
            'marketOpportunity': {
                "totalMarket": f"${market_size:,} global market for {main_trend} solutions",
                "serviceableMarket": f"${int(market_size*0.3):,} addressable with our solution",
                "targetMarket": f"${int(market_size*0.05):,} initial target market",
                "growthDrivers": [
                    "Digital transformation initiatives",
                    "Remote work acceleration",
                    "AI adoption in business processes"
                ],
                "marketDynamics": "Rapid consolidation with demand for specialized solutions"
            },
            
            'riskAnalysis': {
                "marketRisks": ["Economic downturn reducing IT budgets", "Slower adoption than expected"],
                "competitiveRisks": ["Large players entering the market", "Price competition"],
                "technicalRisks": ["Scaling challenges", "Security vulnerabilities"],
                "mitigationStrategies": {
                    "market": "Focus on ROI-driven messaging and flexible pricing",
                    "competitive": "Build strong differentiation and customer loyalty",
                    "technical": "Invest in robust architecture and security practices"
                }
            }
        }
        
        return templates.get(field, {"description": "Detailed analysis required for this section."})

    def generate_executive_summary(self, idea: SaaSIdea, financial_analysis: Dict[str, Any], plan_content: Dict[str, Any]) -> str:
        """Tüm verilere dayanarak bir yönetici özeti oluşturur."""
        revenue = financial_analysis.get('revenue_projections', {})
        year_3_revenue = revenue.get('year_3_target', 1_000_000)
        
        summary = f"""{idea.title} is a SaaS solution addressing critical pain points for mid-market companies. With a projected Year 3 revenue of ${year_3_revenue:,}, our platform is poised for significant growth by offering a unique competitive advantage through advanced AI and a superior user experience."""
        return ' '.join(summary.split())

    def create_financial_highlights(self, financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Finansal analizin kilit noktalarını özetleyen bir sözlük oluşturur."""
        metrics = financial_analysis.get('financial_metrics', {})
        revenue = financial_analysis.get('revenue_projections', {})
        ltv_cac_ratio = metrics.get('ltv_cac_ratio', 3.0)

        return {
            'market_size': f"${metrics.get('market_size', 0):,}",
            'year_3_revenue_target': f"${revenue.get('year_3_target', 0):,}",
            'target_acv': f"${metrics.get('acv', 0):,}", 
            'target_cac': f"${metrics.get('cac', 0):,}",
            'ltv_to_cac_ratio': f"{ltv_cac_ratio:.1f}:1"
        }

    def create_mvp_roadmap_from_analysis(self, idea: SaaSIdea, financial_analysis: Dict[str, Any]) -> List[str]:
        """Analize dayalı dinamik bir MVP yol haritası oluşturur."""
        risk_level = financial_analysis.get('market_analysis', {}).get('risk_level', 'medium')
        timeline = {'low': (1, 3, 5), 'medium': (2, 4, 6), 'high': (2, 5, 8)}
        research, dev, beta = timeline[risk_level]
        return [
            f"Months 1-{research}: Conduct market validation and customer discovery.",
            f"Months {research+1}-{dev}: Develop the core MVP features.",
            f"Month {dev+1}: Launch a private beta with pilot customers.",
            f"Month {beta+1}: Go-to-market launch and begin customer acquisition."
        ]
        
    def get_generation_stats(self) -> Dict[str, int]:
        """Agent'ın çalışma istatistiklerini döndürür."""
        return self.generation_stats.copy()

    def reset_stats(self):
        """İstatistikleri sıfırlar."""
        self.generation_stats = {
            'plans_generated': 0, 'llm_calls_made': 0,
            'json_parse_successes': 0, 'json_parse_failures': 0,
            'fallback_plans_created': 0
        }