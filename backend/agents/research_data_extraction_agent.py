# data_extraction_agent.py
import re
from typing import Dict, Any, List, Union
from base_agent import BaseAgent


class DataExtractionAgent(BaseAgent):
    """
    Veri Çıkarma Agent'ı - Ham arama sonuçlarından yapılandırılmış sayısal verileri çıkarır
    """
    
    def __init__(self):
        super().__init__()
        self.extraction_stats = {
            'successful_extractions': 0,
            'failed_extractions': 0,
            'fallback_used': 0
        }

    def parse_value_from_search_results(
        self, 
        results: List[Dict[str, Any]], 
        keywords: List[str], 
        default_value: Union[int, float],
        metric_type: str = "generic"
    ) -> Union[int, float]:
        """
        Ana veri çıkarma fonksiyonu - gelişmiş ayrıştırma ile
        
        Args:
            results: Ham arama sonuçları
            keywords: Aranacak anahtar kelimeler
            default_value: Bulunamazsa kullanılacak varsayılan değer
            metric_type: Metrik türü (churn, market_size, acv, cac)
            
        Returns:
            Çıkarılan sayısal değer veya varsayılan değer
        """
        if not results:
            print(f"⚠️ [DataExtraction] No results to parse for {metric_type}. Using default: {default_value:,}")
            self.extraction_stats['fallback_used'] += 1
            return default_value
        
        print(f"🔍 [DataExtraction] Parsing {metric_type} from {len(results)} results with keywords: {keywords}")
        
        # Metrik türüne özel işlem
        is_churn_metric = metric_type.lower() in ['churn', 'churn_rate', 'retention']
        is_percentage_metric = is_churn_metric or metric_type.lower() in ['percentage', 'rate']
        
        for i, result in enumerate(results):
            # İçerik birleştirme
            content_parts = [
                result.get('snippet', ''),
                result.get('title', ''),
                result.get('description', ''),
                result.get('url', '')
            ]
            content = " ".join(filter(None, content_parts)).lower()
            
            # Debug info (ilk 3 sonuç için)
            if i < 3:
                print(f"🔍 [DataExtraction] Analyzing result {i+1}: {content[:100]}...")
            
            # Anahtar kelime kontrolü
            if not self._contains_keywords(content, keywords):
                continue
                
            print(f"✅ [DataExtraction] Keywords found in result {i+1}")
            
            # Metrik türüne göre değer çıkarma
            extracted_value = self._extract_value_by_type(content, metric_type, is_percentage_metric)
            
            if extracted_value is not None:
                # Değeri validate et
                if self._validate_extracted_value(extracted_value, metric_type):
                    print(f"✅ [DataExtraction] Successfully extracted {metric_type}: {extracted_value}")
                    self.extraction_stats['successful_extractions'] += 1
                    return extracted_value
        
        print(f"⚠️ [DataExtraction] Could not extract {metric_type} from search results. Using default: {default_value:,}")
        self.extraction_stats['failed_extractions'] += 1
        return default_value

    def _contains_keywords(self, content: str, keywords: List[str]) -> bool:
        """İçerikte anahtar kelimelerden en az birinin bulunup bulunmadığını kontrol eder"""
        for keyword in keywords:
            if keyword.lower() in content:
                return True
        return False

    def _extract_value_by_type(self, content: str, metric_type: str, is_percentage: bool) -> Union[int, float, None]:
        """Metrik türüne göre özelleştirilmiş değer çıkarma"""
        
        if metric_type.lower() in ['churn', 'churn_rate']:
            return self._extract_churn_rate(content)
        elif metric_type.lower() in ['market_size', 'market_value']:
            return self._extract_market_size(content)
        elif metric_type.lower() in ['acv', 'annual_contract_value']:
            return self._extract_currency_value(content, 'acv')
        elif metric_type.lower() in ['cac', 'customer_acquisition_cost']:
            return self._extract_currency_value(content, 'cac')
        else:
            # Genel değer çıkarma
            return self._extract_generic_value(content, is_percentage)

    def _extract_churn_rate(self, content: str) -> Union[float, None]:
        """Churn rate özel çıkarıcı - yüzde değerleri öncelikli"""
        
        # Önce yüzde pattern'leri ara
        percent_patterns = [
            r'(\d+\.?\d*)\s*%',
            r'(\d+\.?\d*)\s*percent',
            r'(\d+\.?\d*)\s*pct'
        ]
        
        for pattern in percent_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match.group(1))
                    # Makul churn rate aralığı: 0.1% - 50%
                    if 0.1 <= value <= 50:
                        return value  # Yüzde olarak döndür
                except (ValueError, TypeError):
                    continue
        
        # Decimal format ara (0.05 = 5%)
        decimal_pattern = r'\b0\.(\d+)\b'
        matches = re.finditer(decimal_pattern, content)
        for match in matches:
            try:
                decimal_value = float(match.group(0))
                if 0.001 <= decimal_value <= 0.5:  # 0.1% - 50% aralığı
                    return decimal_value * 100  # Yüzdeye çevir
            except (ValueError, TypeError):
                continue
        
        return None

    def _extract_market_size(self, content: str) -> Union[int, None]:
        """Market size özel çıkarıcı - büyük sayılar ve para birimleri"""
        
        # Market size için pattern'ler (büyükten küçüğe öncelik)
        patterns = [
            # Trillion formats
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*trillion',
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*T\b',
            
            # Billion formats  
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*billion',
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*B\b',
            
            # Million formats
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*million',
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*M\b',
            
            # Direct currency amounts
            r'[£$€¥]\s*([\d,]+\.?\d*)\b'
        ]
        
        multipliers = {
            'trillion': 1_000_000_000_000,
            't': 1_000_000_000_000,
            'billion': 1_000_000_000,
            'b': 1_000_000_000,
            'million': 1_000_000,
            'm': 1_000_000
        }
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    base_num = float(match.group(1).replace(',', ''))
                    
                    # Multiplier'ı belirle
                    multiplier = 1
                    full_match = match.group(0).lower()
                    for unit, mult in multipliers.items():
                        if unit in full_match:
                            multiplier = mult
                            break
                    
                    value = int(base_num * multiplier)
                    
                    # Market size için makul aralık: 1M - 10T
                    if 1_000_000 <= value <= 10_000_000_000_000:
                        return value
                        
                except (ValueError, TypeError):
                    continue
        
        return None

    def _extract_currency_value(self, content: str, value_type: str) -> Union[int, None]:
        """Para birimi değerleri için çıkarıcı (ACV, CAC)"""
        
        patterns = [
            # Currency with units
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*(?:thousand|k)\b',
            r'[£$€¥]?\s*([\d,]+\.?\d*)\s*(?:million|m)\b',
            
            # Direct currency amounts
            r'[£$€¥]\s*([\d,]+\.?\d*)\b',
            
            # Numbers with currency words
            r'\b([\d,]+\.?\d*)\s*(?:dollars?|usd|gbp|eur|pounds?)\b'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                try:
                    base_num = float(match.group(1).replace(',', ''))
                    
                    # Unit multiplier
                    multiplier = 1
                    full_match = match.group(0).lower()
                    if any(unit in full_match for unit in ['thousand', 'k']):
                        multiplier = 1_000
                    elif any(unit in full_match for unit in ['million', 'm']):
                        multiplier = 1_000_000
                    
                    value = int(base_num * multiplier)
                    
                    # Değer tipine göre makul aralıklar
                    if value_type.lower() == 'acv' and 100 <= value <= 1_000_000:
                        return value
                    elif value_type.lower() == 'cac' and 50 <= value <= 100_000:
                        return value
                    elif 100 <= value <= 10_000_000:  # Genel aralık
                        return value
                        
                except (ValueError, TypeError):
                    continue
        
        return None

    def _extract_generic_value(self, content: str, is_percentage: bool) -> Union[int, float, None]:
        """Genel değer çıkarıcı"""
        
        if is_percentage:
            # Yüzde değerleri için
            pattern = r'(\d+\.?\d*)\s*%'
            matches = re.finditer(pattern, content)
            for match in matches:
                try:
                    value = float(match.group(1))
                    if 0 <= value <= 100:
                        return value
                except (ValueError, TypeError):
                    continue
        
        # Sayısal değerler için genel pattern
        pattern = r'\b([\d,]+\.?\d*)\b'
        matches = re.finditer(pattern, content)
        for match in matches:
            try:
                value = float(match.group(1).replace(',', ''))
                if value > 0:
                    return int(value) if value == int(value) else value
            except (ValueError, TypeError):
                continue
        
        return None

    def _validate_extracted_value(self, value: Union[int, float], metric_type: str) -> bool:
        """Çıkarılan değerin metrik türü için makul olup olmadığını kontrol eder"""
        
        validation_rules = {
            'churn': lambda v: 0.1 <= v <= 50,  # Yüzde olarak
            'churn_rate': lambda v: 0.1 <= v <= 50,
            'market_size': lambda v: 1_000_000 <= v <= 10_000_000_000_000,
            'acv': lambda v: 100 <= v <= 1_000_000,
            'cac': lambda v: 50 <= v <= 100_000,
            'generic': lambda v: v > 0
        }
        
        validator = validation_rules.get(metric_type.lower(), validation_rules['generic'])
        
        try:
            return validator(value)
        except:
            return False

    def extract_multiple_metrics(
        self, 
        results_by_metric: Dict[str, List[Dict[str, Any]]], 
        keywords_by_metric: Dict[str, List[str]], 
        defaults: Dict[str, Union[int, float]]
    ) -> Dict[str, Union[int, float]]:
        """
        Birden fazla metrik için toplu çıkarma işlemi
        
        Args:
            results_by_metric: Metrik türü -> Arama sonuçları
            keywords_by_metric: Metrik türü -> Anahtar kelimeler  
            defaults: Metrik türü -> Varsayılan değerler
            
        Returns:
            Metrik türü -> Çıkarılan değerler
        """
        extracted_values = {}
        
        for metric_type in results_by_metric.keys():
            results = results_by_metric[metric_type]
            keywords = keywords_by_metric.get(metric_type, [])
            default = defaults.get(metric_type, 0)
            
            extracted_values[metric_type] = self.parse_value_from_search_results(
                results, keywords, default, metric_type
            )
        
        # İstatistikleri yazdır
        print(f"📊 [DataExtraction] Extraction complete:")
        print(f"  ✅ Successful: {self.extraction_stats['successful_extractions']}")
        print(f"  ❌ Failed: {self.extraction_stats['failed_extractions']}")
        print(f"  🔄 Fallback used: {self.extraction_stats['fallback_used']}")
        
        return extracted_values

    def get_extraction_stats(self) -> Dict[str, int]:
        """Çıkarma istatistiklerini döndürür"""
        return self.extraction_stats.copy()

    def reset_stats(self):
        """İstatistikleri sıfırlar"""
        self.extraction_stats = {
            'successful_extractions': 0,
            'failed_extractions': 0,
            'fallback_used': 0
        }


# Test fonksiyonu
def test_data_extraction_agent():
    """DataExtractionAgent test fonksiyonu"""
    print("🧪 Testing DataExtractionAgent...")
    
    agent = DataExtractionAgent()
    
    # Test verileri
    test_results = [
        {
            'title': 'SaaS Market Size Analysis 2024',
            'snippet': 'The global SaaS market is valued at $250 billion and growing at 15% annually.',
            'url': 'https://example.com/saas-market'
        },
        {
            'title': 'Customer Acquisition Costs in B2B',
            'snippet': 'Average CAC for B2B SaaS companies ranges from $1,500 to $5,000 per customer.',
            'url': 'https://example.com/cac-analysis'
        },
        {
            'title': 'SaaS Churn Rate Benchmarks',
            'snippet': 'Industry average churn rate is 8.5% annually for enterprise SaaS.',
            'url': 'https://example.com/churn-benchmarks'
        }
    ]
    
    # Test 1: Market size çıkarma
    market_size = agent.parse_value_from_search_results(
        test_results, 
        ['market size', 'market value'], 
        100_000_000, 
        'market_size'
    )
    print(f"Test 1 - Market size: ${market_size:,}")
    
    # Test 2: CAC çıkarma
    cac = agent.parse_value_from_search_results(
        test_results, 
        ['customer acquisition cost', 'cac'], 
        2000, 
        'cac'
    )
    print(f"Test 2 - CAC: ${cac:,}")
    
    # Test 3: Churn rate çıkarma
    churn = agent.parse_value_from_search_results(
        test_results, 
        ['churn rate', 'churn'], 
        10, 
        'churn'
    )
    print(f"Test 3 - Churn: {churn}%")
    
    # İstatistikleri göster
    stats = agent.get_extraction_stats()
    print(f"📊 Extraction stats: {stats}")

if __name__ == "__main__":
    test_data_extraction_agent()