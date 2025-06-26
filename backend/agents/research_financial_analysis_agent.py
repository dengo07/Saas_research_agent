# financial_analysis_agent.py
from typing import Dict, Any, List, Union
from base_agent import BaseAgent
from models import RiskLevel, FinancialMetrics, SearchResultQuality

class FinancialAnalysisAgent(BaseAgent):
    """
    Finansal Analiz Agent'ı - Çıkarılmış metriklerden analiz ve projeksiyonlar üretir
    """
    
    def __init__(self):
        super().__init__()
        self.analysis_metadata = {
            'calculations_performed': 0,
            'projections_created': 0,
            'risk_assessments': 0
        }

    def analyze_financial_metrics(
        self, 
        extracted_metrics: Dict[str, Union[int, float]],
        competitor_count: int, # MODIFIED: Added competitor_count as a required input
        search_quality_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Ana finansal analiz fonksiyonu - tüm analizleri koordine eder
        """
        print("📊 [FinancialAnalysis] Starting comprehensive financial analysis...")
        
        normalized_metrics = self._normalize_and_validate_metrics(extracted_metrics)
        
        # MODIFIED: Pass competitor_count to the analysis functions
        market_analysis = self._analyze_market_difficulty(normalized_metrics, competitor_count)
        revenue_projections = self._create_revenue_projections(normalized_metrics, market_analysis)
        
        # MODIFIED: This now creates the correct data structure for the frontend chart
        competitive_analysis = self._create_competitive_analysis(normalized_metrics, market_analysis, competitor_count)
        
        visualization_data = self._create_visualization_data(normalized_metrics, revenue_projections)
        health_score = self._calculate_financial_health_score(normalized_metrics, market_analysis)
        search_quality = self._assess_search_quality(search_quality_data) if search_quality_data else None
        
        analysis_result = {
            'financial_metrics': normalized_metrics,
            'market_analysis': market_analysis,
            'revenue_projections': revenue_projections,
            # This key is now passed to the BusinessPlanWriterAgent with the correct structure
            'competitiveAnalysis': competitive_analysis, 
            'visualization_data': visualization_data,
            'health_score': health_score,
            'search_quality': search_quality,
            'analysis_metadata': self.analysis_metadata.copy()
        }
        
        self.analysis_metadata['calculations_performed'] += 1
        print("✅ [FinancialAnalysis] Comprehensive analysis completed")
        
        return analysis_result

    def _normalize_and_validate_metrics(self, metrics: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        """Metrikleri normalize et ve geçersiz değerleri düzelt"""
        
        defaults = {
            'market_size': 250_000_000,
            'acv': 8000,
            'cac': 2500,
            'churn': 10
        }
        
        normalized = {}
        
        for key, value in metrics.items():
            if value is None or value <= 0:
                print(f"⚠️ [FinancialAnalysis] Invalid {key}: {value}, using default: {defaults.get(key, 0)}")
                normalized[key] = defaults.get(key, 0)
            else:
                normalized[key] = value
        
        if 'churn' in normalized and normalized['churn'] > 1:
            normalized['churn_decimal'] = normalized['churn'] / 100.0
        else:
            normalized['churn_decimal'] = normalized.get('churn', 0.10)
        
        if normalized.get('cac', 0) > 0 and normalized.get('acv', 0) > 0:
            ltv_cac_ratio = (normalized['acv'] / normalized['churn_decimal']) / normalized['cac']
            normalized['ltv_cac_ratio'] = ltv_cac_ratio
            
            if ltv_cac_ratio < 3:
                print(f"⚠️ [FinancialAnalysis] Low LTV:CAC ratio: {ltv_cac_ratio:.1f} (healthy > 3)")
        
        print(f"📊 [FinancialAnalysis] Normalized metrics: Market(${normalized.get('market_size', 0):,}), ACV(${normalized.get('acv', 0):,}), CAC(${normalized.get('cac', 0):,}), Churn({normalized.get('churn_decimal', 0):.1%})")
        
        return normalized

    def _analyze_market_difficulty(self, metrics: Dict[str, Union[int, float]], competitor_count: int) -> Dict[str, Any]: # MODIFIED: Added competitor_count
        """Market zorluğu analizi"""
        
        market_size = metrics.get('market_size', 250_000_000)
        acv = metrics.get('acv', 8000)
        cac = metrics.get('cac', 2500)
        churn_decimal = metrics.get('churn_decimal', 0.10)
        
        # Market size difficulty (0-1 scale)
        if market_size < 10_000_000:
            size_difficulty = 0.8
            size_category = "niche"
        elif market_size < 100_000_000:
            size_difficulty = 0.3
            size_category = "emerging"
        elif market_size < 1_000_000_000:
            size_difficulty = 0.4
            size_category = "established"
        else:
            size_difficulty = 0.7
            size_category = "mature"
        
        # NEW: Competitor Difficulty
        if competitor_count > 10:
            competitor_difficulty = 0.8
        elif competitor_count > 5:
            competitor_difficulty = 0.6
        else:
            competitor_difficulty = 0.3

        # CAC/ACV ratio difficulty
        cac_acv_ratio = cac / acv if acv > 0 else 1.0
        if cac_acv_ratio > 0.5:
            acquisition_difficulty = 0.8
        elif cac_acv_ratio > 0.3:
            acquisition_difficulty = 0.6
        else:
            acquisition_difficulty = 0.3
        
        # Churn difficulty
        if churn_decimal > 0.15:
            retention_difficulty = 0.8
        elif churn_decimal > 0.10:
            retention_difficulty = 0.5
        else:
            retention_difficulty = 0.3
        
        # MODIFIED: Overall difficulty score now includes competitor difficulty
        overall_difficulty = (
            size_difficulty * 0.30 + 
            competitor_difficulty * 0.30 + # New weight
            acquisition_difficulty * 0.25 + 
            retention_difficulty * 0.15
        )
        
        # Risk level based on the new, more accurate score
        if overall_difficulty < 0.4: # Adjusted threshold
            risk_level = RiskLevel.LOW
            risk_description = "Low risk market with favorable conditions"
        elif overall_difficulty < 0.65: # Adjusted threshold
            risk_level = RiskLevel.MEDIUM
            risk_description = "Medium risk market requiring strategic execution"
        else:
            risk_level = RiskLevel.HIGH
            risk_description = "High risk market with significant challenges"
        
        self.analysis_metadata['risk_assessments'] += 1
        
        return {
            'overall_difficulty': overall_difficulty,
            'competitor_difficulty': competitor_difficulty, # New
            'size_difficulty': size_difficulty,
            'acquisition_difficulty': acquisition_difficulty,
            'retention_difficulty': retention_difficulty,
            'size_category': size_category,
            'risk_level': risk_level,
            'risk_description': risk_description,
            'cac_acv_ratio': cac_acv_ratio,
            'market_attractiveness': max(0, min(100, 90 - (overall_difficulty * 60)))
        }

    # ... (The _create_revenue_projections method does not need changes) ...
    def _create_revenue_projections(self, metrics: Dict[str, Union[int, float]], market_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """5 yıllık gelir projeksiyonu oluştur"""
        
        acv = metrics.get('acv', 8000)
        cac = metrics.get('cac', 2500)
        churn_decimal = metrics.get('churn_decimal', 0.10)
        difficulty = market_analysis.get('overall_difficulty', 0.5)
        
        initial_budget = max(5 * cac, 50_000)
        base_growth_rate = max(1.2, 2.0 - (difficulty * 0.6))
        
        projections = {
            'labels': ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5"],
            'revenue': [], 'customers': [], 'marketing_budget': [], 'growth_rates': []
        }
        
        customer_count = 0
        current_budget = initial_budget
        previous_revenue = 0
        
        for year in range(5):
            retained_customers = customer_count * (1 - churn_decimal)
            new_customers = max(1, current_budget / cac)
            customer_count = retained_customers + new_customers
            current_revenue = customer_count * acv
            
            if year > 0 and previous_revenue > 0:
                growth_rate = ((current_revenue - previous_revenue) / previous_revenue) * 100
            else:
                growth_rate = 0
            
            projections['revenue'].append(int(current_revenue))
            projections['customers'].append(int(customer_count))
            projections['marketing_budget'].append(int(current_budget))
            projections['growth_rates'].append(round(growth_rate, 1))
            
            previous_revenue = current_revenue
            current_budget *= base_growth_rate
        
        projections['total_5_year_revenue'] = sum(projections['revenue'])
        projections['year_3_target'] = projections['revenue'][2]
        projections['final_customer_count'] = projections['customers'][-1]
        projections['average_growth_rate'] = sum(projections['growth_rates'][1:]) / 4
        
        self.analysis_metadata['projections_created'] += 1
        print(f"📈 [FinancialAnalysis] 5-year revenue projection: {[f'${r:,.0f}' for r in projections['revenue']]}")
        return projections

    # NEW: This entire function is replaced to create the correct data structure for the frontend.
    def _create_competitive_analysis(self, metrics: Dict[str, Union[int, float]], market_analysis: Dict[str, Any], competitor_count: int) -> Dict[str, Any]:
        """
        Rekabet analizi ve skorları, frontend radar chart için veri yapısı oluşturur.
        """
        difficulty = market_analysis.get('competitor_difficulty', 0.5)
        
        # Market position based on competitor count
        if competitor_count > 10:
            position = 'challenging'
        elif competitor_count > 5:
            position = 'competitive'
        else:
            position = 'emerging'
        
        # Competitive scores
        base_score = 70
        innovation_boost = 15 # Assuming the new idea is innovative
        difficulty_penalty = int(difficulty * 20)
        
        scores = {
            'innovation': max(50, min(100, base_score + innovation_boost - difficulty_penalty)),
            'quality': max(60, min(100, base_score + 5 - difficulty_penalty)),
            'pricing': max(55, min(100, base_score - 5 - difficulty_penalty))
        }
        
        # This is the exact data structure the frontend `renderCompetitiveRadarChart` function needs
        radar_data = {
            'labels': ['Price', 'Features', 'Quality', 'Marketing', 'Innovation'],
            'yourBusiness': [
                scores['pricing'],
                scores['innovation'] - 5,  # Features are slightly behind pure innovation
                scores['quality'],
                max(50, base_score - 10),  # Marketing starts lower
                scores['innovation']
            ],
            'competitorAvg': [70, 75, 80, 85, 70] # Static competitor average
        }
        
        # Return a dictionary that includes the radar data directly
        return {
            'market_position': position,
            'differentiation_score': max(60, 100 - int(difficulty * 40)),
            'competitive_intensity': difficulty,
            'scores': scores,
            # Pass the chart data in the expected keys
            'labels': radar_data['labels'],
            'yourBusiness': radar_data['yourBusiness'], 
            'competitorAvg': radar_data['competitorAvg']
        }

    # ... (The remaining methods do not need changes) ...
    def _create_visualization_data(self, metrics: Dict[str, Union[int, float]], projections: Dict[str, Any]) -> Dict[str, Any]:
        """Görselleştirme için veri hazırla"""
        
        market_size = metrics.get('market_size', 250_000_000)
        tam = market_size
        sam = int(tam * 0.15)
        som = int(sam * 0.05)
        
        market_data = {
            'labels': ['TAM', 'SAM', 'SOM'],
            'values': [tam, sam, som],
            'colors': ['#8b5cf6', '#a855f7', '#c084fc']
        }
        
        health_metrics = {
            'labels': ['Revenue Growth', 'Customer Acquisition', 'Retention', 'Market Size', 'Profitability'],
            'values': [
                min(100, max(0, projections.get('average_growth_rate', 50))),
                min(100, max(0, 100 - (metrics.get('cac', 2500) / 50))),
                min(100, max(0, (1 - metrics.get('churn_decimal', 0.10)) * 100)),
                min(100, max(0, (market_size / 10_000_000))),
                min(100, max(0, metrics.get('ltv_cac_ratio', 3) * 20))
            ]
        }
        
        return {
            'market_data': market_data,
            'revenue_data': { 'labels': projections['labels'], 'revenue': projections['revenue'] },
            'health_metrics': health_metrics,
            'key_metrics': {
                'market_size': market_size,
                'year_3_revenue': projections.get('year_3_target', 0),
                'ltv_cac_ratio': metrics.get('ltv_cac_ratio', 0),
                'customer_lifetime': 1 / metrics.get('churn_decimal', 0.10) if metrics.get('churn_decimal', 0) > 0 else 10
            }
        }

    def _calculate_financial_health_score(self, metrics: Dict[str, Union[int, float]], market_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Genel finansal sağlık skoru hesapla"""
        scores = {
            'market_opportunity': max(0, min(100, (metrics.get('market_size', 0) / 10_000_000))),
            'unit_economics': max(0, min(100, metrics.get('ltv_cac_ratio', 0) * 20)),
            'customer_retention': max(0, min(100, (1 - metrics.get('churn_decimal', 0.10)) * 100)),
            'market_risk': max(0, min(100, 100 - (market_analysis.get('overall_difficulty', 0.5) * 100)))
        }
        weights = { 'market_opportunity': 0.25, 'unit_economics': 0.30, 'customer_retention': 0.25, 'market_risk': 0.20 }
        overall_score = sum(scores[key] * weights[key] for key in scores.keys())
        
        if overall_score >= 80:
            health_category, health_description = "Excellent", "Strong fundamentals with high growth potential"
        elif overall_score >= 65:
            health_category, health_description = "Good", "Solid foundation with manageable risks"
        elif overall_score >= 50:
            health_category, health_description = "Fair", "Viable but requires strategic improvements"
        else:
            health_category, health_description = "Poor", "Significant challenges requiring major adjustments"
        
        return {
            'overall_score': round(overall_score, 1),
            'component_scores': scores,
            'health_category': health_category,
            'health_description': health_description,
            'confidence_level': max(70, min(95, overall_score + 10))
        }

    def _assess_search_quality(self, search_data: Dict[str, Any]) -> SearchResultQuality:
        """Arama kalitesini değerlendir"""
        try:
            return SearchResultQuality(**search_data)
        except Exception as e:
            print(f"⚠️ [FinancialAnalysis] Search quality assessment failed: {e}")
            return None

    def get_analysis_metadata(self) -> Dict[str, int]:
        return self.analysis_metadata.copy()
