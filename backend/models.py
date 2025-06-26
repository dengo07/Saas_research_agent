import datetime
from pydantic import BaseModel, Field, validator,computed_field
from typing import Dict, Any, List, Optional,Union
from enum import Enum

class ResearchQuery(BaseModel):
    query: str = Field(..., min_length=2, max_length=200)
    include_reddit: bool = True
    include_trends: bool = True
    include_competitors: bool = True
    depth: str = "standard"

class SaaSIdea(BaseModel):
    title: str
    description: str
    source: str
    potential: int = Field(..., ge=1, le=10)
    tags: List[str]
    validation: str
    marketSize: str
    painPoints: List[str]
    competitors: List[str] = []
    trends: List[str] = []
    reddit_insights: Optional[str] = None

class RiskLevel(str, Enum):
    """Risk seviyeleri için tutarlılığı sağlayan Enum."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class FinancialMetrics(BaseModel):
    """Finansal metrikler için ayrı ve doğrulanmış model."""
    market_size: int = Field(..., ge=1000000, description="USD cinsinden Toplam Adreslenebilir Pazar")
    acv: int = Field(..., ge=100, description="USD cinsinden Yıllık Kontrat Değeri")
    cac: int = Field(..., ge=50, description="USD cinsinden Müşteri Edinme Maliyeti")
    churn_rate: float = Field(..., ge=0.01, le=0.5, description="Yıllık churn oranı (ondalık)")


# Also update the BusinessPlan model to accept optional dict fields
class BusinessPlan(BaseModel):
    """Enhanced BusinessPlan model with better validation and structure"""
    
    # Core business plan content - FIXED: All structured fields as dict
    targetAudience: Dict[str, Any] = Field(..., description="Detailed target audience description with structure")
    coreFeatures: Dict[str, Any] = Field(..., description="Core product features with structure")
    monetizationModel: Dict[str, Any] = Field(..., description="Revenue and pricing strategy")
    marketingStrategy: Dict[str, Any] = Field(..., description="Go-to-market strategy")
    competitiveAdvantage: Dict[str, Any] = Field(..., description="Key differentiators")
    researchInsights: Dict[str, Any] = Field(..., description="Market research findings with structure")
    painPointsAddressed: Dict[str, Any] = Field(..., description="How solution addresses pain points")
    marketOpportunity: Dict[str, Any] = Field(..., description="Market size and opportunity analysis")
    riskAnalysis: Dict[str, Any] = Field(..., description="Risk assessment and mitigation")
    
    # Summary fields - these can remain as strings
    executiveSummary: Optional[str] = Field(None, description="Executive summary of the business plan")
    financialHighlights: Optional[Dict[str, Any]] = Field(None, description="Key financial metrics and highlights")
    
    # MVP and timeline
    mvpRoadmap: List[str] = Field(..., min_items=3, description="MVP development roadmap")
    mvpTimeframe: int = Field(default=6, ge=3, le=24, description="Time to MVP in months")
    
    # Market and competition metrics
    competitorCount: int = Field(default=0, ge=0, description="Number of direct competitors")
    marketSize: int = Field(default=100000000, ge=1000000, description="TAM as an integer")
    confidenceScore: int = Field(default=75, ge=0, le=100, description="Confidence score percentage")
    riskLevel: RiskLevel = Field(default=RiskLevel.MEDIUM, description="Overall risk level")
    
    # Financial projections
    targetRevenue: int = Field(default=1000000, ge=10000, description="Target revenue for Year 3")
    financialMetrics: Optional[Dict[str, Any]] = Field(None, description="Detailed financial metrics as dict")
    
    # Visualization data with validation
    marketData: Dict[str, Any] = Field(..., description="Market size visualization data")
    revenueData: Dict[str, Any] = Field(..., description="Revenue projection data")
    competitiveData: Dict[str, Any] = Field(..., description="Competitive analysis data")
    competitiveScores: Dict[str, int] = Field(..., description="Competitive scoring data")
    
    # Optional metadata
    dataSource: Optional[str] = Field(default="web_search", description="Source of market data")
    lastUpdated: Optional[str] = Field(None, description="When the plan was generated")
    searchQuality: Optional[Dict[str, Any]] = Field(None, description="Quality metrics for search results as dict")
    
    @validator('targetAudience')
    def validate_target_audience(cls, v):
        """Validate target audience structure"""
        required_keys = ['primary', 'demographics']
        if not all(key in v for key in required_keys):
            print(f"⚠️ targetAudience missing required keys: {required_keys}")
        return v
    
    @validator('coreFeatures') 
    def validate_core_features(cls, v):
        """Validate core features structure"""
        if not isinstance(v, dict):
            raise ValueError("coreFeatures must be a dictionary")
        return v
    
    @validator('monetizationModel')
    def validate_monetization_model(cls, v):
        """Validate monetization model structure"""
        required_keys = ['type', 'pricingStrategy']
        if not all(key in v for key in required_keys):
            print(f"⚠️ monetizationModel missing required keys: {required_keys}")
        return v
    
    @validator('marketingStrategy')
    def validate_marketing_strategy(cls, v):
        """Validate marketing strategy structure"""
        if not isinstance(v, dict):
            raise ValueError("marketingStrategy must be a dictionary")
        return v
    
    @validator('competitiveAdvantage')
    def validate_competitive_advantage(cls, v):
        """Validate competitive advantage structure"""
        if not isinstance(v, dict):
            raise ValueError("competitiveAdvantage must be a dictionary")
        return v
    
    @validator('researchInsights')
    def validate_research_insights(cls, v):
        """Validate research insights structure"""
        if not isinstance(v, dict):
            raise ValueError("researchInsights must be a dictionary")
        return v
    
    @validator('painPointsAddressed')
    def validate_pain_points(cls, v):
        """Validate pain points structure"""
        if not isinstance(v, dict):
            raise ValueError("painPointsAddressed must be a dictionary")
        return v
    
    @validator('riskAnalysis')
    def validate_risk_analysis(cls, v):
        """Validate risk analysis structure"""
        if not isinstance(v, dict):
            raise ValueError("riskAnalysis must be a dictionary")
        return v
    
    @validator('marketData')
    def validate_market_data(cls, v):
        """Validate market data structure"""
        required_keys = ['labels', 'values', 'colors']
        if not all(key in v for key in required_keys):
            print(f"⚠️ marketData missing required keys: {required_keys}")
            # Auto-fix missing keys
            v.setdefault('labels', ['TAM', 'SAM', 'SOM'])
            v.setdefault('values', [250000000, 75000000, 15000000])
            v.setdefault('colors', ['#3B82F6', '#10B981', '#F59E0B'])
        
        # Ensure TAM >= SAM >= SOM
        values = v.get('values', [])
        if len(values) >= 3 and not (values[0] >= values[1] >= values[2]):
            print("⚠️ Fixing market values order (TAM >= SAM >= SOM)")
            values.sort(reverse=True)
            v['values'] = values
        
        return v
    
    @validator('revenueData')
    def validate_revenue_data(cls, v):
        """Validate revenue data structure"""
        required_keys = ['labels', 'revenue']
        if not all(key in v for key in required_keys):
            print(f"⚠️ revenueData missing required keys: {required_keys}")
            # Auto-fix missing keys
            v.setdefault('labels', ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5'])
            v.setdefault('revenue', [100000, 500000, 1500000, 3000000, 5000000])
        
        # Ensure revenue projection shows overall growth
        revenue = v.get('revenue', [])
        if len(revenue) >= 2 and revenue[-1] <= revenue[0]:
            print("⚠️ Revenue projection should show growth - auto-fixing")
            # Create a growth pattern
            start_revenue = revenue[0] if revenue else 100000
            v['revenue'] = [start_revenue * (1.5 ** i) for i in range(len(revenue) or 5)]
        
        return v
    
    @validator('competitiveData')
    def validate_competitive_data(cls, v):
        """Validate competitive data structure - Frontend radar chart format"""
        required_keys = ['labels', 'yourBusiness', 'competitorAvg']
        if not all(key in v for key in required_keys):
            print(f"⚠️ competitiveData missing required keys: {required_keys}")
            # Auto-fix for radar chart format
            v.setdefault('labels', ['Price', 'Features', 'Quality', 'Marketing', 'Innovation'])
            v.setdefault('yourBusiness', [75, 85, 80, 60, 90])
            v.setdefault('competitorAvg', [70, 75, 80, 85, 70])
        
        return v
    
    @validator('competitiveScores')
    def validate_competitive_scores(cls, v):
        """Validate competitive scores"""
        required_keys = ['innovation', 'quality', 'pricing']
        if not all(key in v for key in required_keys):
            print(f"⚠️ competitiveScores missing required keys: {required_keys}")
            # Auto-fix missing scores
            v.setdefault('innovation', 75)
            v.setdefault('quality', 80)
            v.setdefault('pricing', 70)
        
        # Ensure all scores are valid percentages
        for key, score in v.items():
            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                print(f"⚠️ Fixing invalid score '{key}': {score}")
                v[key] = max(0, min(100, int(score) if isinstance(score, (int, float)) else 75))
        
        return v
    
    @validator('targetRevenue')
    def validate_revenue_consistency(cls, v, values):
        """Ensure target revenue is consistent with market size"""
        market_size = values.get('marketSize', 0)
        if market_size > 0 and v > market_size * 0.1:  # Target revenue shouldn't exceed 10% of market
            print(f"⚠️ Target revenue {v} seems high for market size {market_size} - adjusting")
            return min(v, int(market_size * 0.05))  # Cap at 5% of market
        return v
    
    class Config:
        extra = 'forbid'  # Prevent unexpected fields
        use_enum_values = True  # Use enum values instead of enum objects
        
        # Example data for documentation
        schema_extra = {
            "example": {
                "targetAudience": {
                    "primary": "Mid-market companies (100-1000 employees)",
                    "demographics": "VPs and Directors, age 35-50",
                    "painPoints": ["manual processes", "lack of insights"]
                },
                "coreFeatures": {
                    "feature1": {
                        "name": "AI Analytics",
                        "description": "Advanced analytics engine",
                        "value": "60% time savings"
                    }
                },
                "monetizationModel": {
                    "type": "SaaS subscription",
                    "pricingStrategy": "Value-based pricing"
                },
                "marketingStrategy": {
                    "channels": ["digital", "partnerships"],
                    "messaging": "Transform your business process"
                },
                "competitiveAdvantage": {
                    "differentiators": ["AI-powered", "Easy to use"],
                    "moat": "Network effects"
                },
                "researchInsights": {
                    "marketTrends": ["AI adoption", "Remote work"],
                    "opportunitySize": "$250M market"
                },
                "painPointsAddressed": {
                    "primary": {
                        "problem": "Manual data entry",
                        "solution": "Automated workflows"
                    }
                },
                "marketOpportunity": {
                    "totalMarket": "$250M TAM",
                    "growthDrivers": ["Digital transformation"]
                },
                "riskAnalysis": {
                    "marketRisks": ["Economic downturn"],
                    "mitigationStrategies": {"market": "Focus on ROI"}
                },
                "marketSize": 250000000,
                "targetRevenue": 5000000,
                "riskLevel": "medium",
                "confidenceScore": 85
            }
        }

# Additional helper models for complex data structures

class SearchResultQuality(BaseModel):
    """Model to track the quality of search results"""
    queries_executed: int = Field(..., ge=0)
    results_found: int = Field(..., ge=0)
    values_extracted: int = Field(..., ge=0)
    fallback_used: int = Field(..., ge=0)
    
    @computed_field
    @property
    def search_success_rate(self) -> float:
        """Auto-calculate success rate based on extracted values vs queries"""
        if self.queries_executed == 0:
            return 0.0
        return min(1.0, self.values_extracted / self.queries_executed)

class BusinessPlanRequest(BaseModel):
    """Request model with validation"""
    idea: 'SaaSIdea'  # Forward reference
    include_search_quality: bool = Field(default=True, description="Include search quality metrics")
    search_timeout: int = Field(default=30, ge=5, le=120, description="Search timeout in seconds")
    
class BusinessPlanResponse(BaseModel):
    """Response wrapper with metadata"""
    business_plan: BusinessPlan
    generation_time: float = Field(..., ge=0, description="Time taken to generate plan in seconds")
    search_quality: Optional[SearchResultQuality] = None
    warnings: List[str] = Field(default_factory=list, description="Any warnings during generation")
    
    class Config:
        extra = 'forbid'