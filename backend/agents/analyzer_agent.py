# agents/analyzer_agent.py
import json
import re
from typing import List, Dict
from base_agent import BaseAgent

class AnalyzerAgent(BaseAgent):
    """Araştırma verilerini analiz edip SaaS fikirleri üreten agent."""
    
    async def generate_saas_ideas(self, query: str, research_context: str) -> List[Dict]:
        print("💡 [Analyzer] Generating SaaS ideas from research data...")
        
        system_prompt = """You are an expert SaaS product strategist. Your goal is to identify viable SaaS opportunities based on the provided market research.
You MUST follow the requested JSON structure precisely. You must return ONLY a valid JSON array, enclosed in a single markdown code block like ```json ... ```. Do not add any text or explanation before or after the markdown block."""
       
        ideas_prompt = f"""
        Based on this market research data for "{query}", generate 3-5 innovative SaaS ideas.
        
        <research_data>
        {research_context}
        </research_data>
       
        You MUST return ONLY a valid JSON array of objects, inside a markdown code block. Each object in the array MUST have these exact keys with the specified data types:
        
        - "title": string (product name)
        - "description": string (detailed description)
        - "source": string (inspiration source)
        - "potential": integer (1-10 scale, where 1=very low, 10=very high potential)
        - "tags": array of strings (relevant tags)
        - "validation": string (how to validate the idea)
        - "marketSize": string (market size information)
        - "painPoints": array of strings (problems it solves)
        
        CRITICAL: The "potential" field MUST be an integer between 1-10, NOT a descriptive string.
        
        Example format:
        ```json
        [
          {{
            "title": "Example SaaS",
            "description": "Description here",
            "source": "Based on research finding X",
            "potential": 8,
            "tags": ["tag1", "tag2"],
            "validation": "How to validate",
            "marketSize": "Market size info",
            "painPoints": ["problem1", "problem2"]
          }}
        ]
        ```
        
        Generate the JSON array inside a ```json ... ``` block now.
        """
       
        llm_response_str = await self.call_llm(ideas_prompt, system_prompt)
       
        try:
            print(f"🤖 Raw response from LLM:\n{llm_response_str}")
            
            # Geliştirilmiş JSON extraction
            json_text = self._extract_json_from_response(llm_response_str)
            
            if not json_text:
                print("❌ [Analyzer] Could not extract JSON from response.")
                return []
            
            print(f"✨ [Analyzer] Cleaned JSON text for parsing:\n{json_text}")
            
            # JSON parse et
            parsed_data = json.loads(json_text)
            
            # Veri yapısını kontrol et ve normalize et
            normalized_data = self._normalize_saas_ideas(parsed_data)
            
            return normalized_data
            
        except json.JSONDecodeError as e:
            print(f"❌ [Analyzer] JSON parse error: {e}")
            print(f"Problematic JSON text: {json_text}")
            return []
        except Exception as e:
            print(f"❌ [Analyzer] Unexpected error: {e}")
            return []
    
    def _extract_json_from_response(self, response: str) -> str:
        """LLM response'undan JSON'ı güvenli şekilde çıkar."""
        
        # 1. Önce markdown JSON block'u ara
        markdown_match = re.search(r'```json\s*(\[.*?\])\s*```', response, re.DOTALL)
        if markdown_match:
            print("✨ [Analyzer] Found markdown JSON block.")
            return markdown_match.group(1).strip()
        
        # 2. Markdown block yoksa, sadece JSON kısmını bul
        # JSON array veya object'i bul
        json_patterns = [
            r'(\[.*\])',  # Array pattern
            r'(\{.*\})'   # Object pattern
        ]
        
        for pattern in json_patterns:
            match = re.search(pattern, response, re.DOTALL)
            if match:
                candidate = match.group(1).strip()
                # Basit bir JSON validation
                if self._is_valid_json_structure(candidate):
                    print(f"✨ [Analyzer] Found JSON with pattern: {pattern}")
                    return candidate
        
        print("⚠️ [Analyzer] No valid JSON structure found.")
        return ""
    
    def _is_valid_json_structure(self, text: str) -> bool:
        """Basit JSON struktur validasyonu."""
        text = text.strip()
        
        # Temel bracket/brace dengesini kontrol et
        if text.startswith('[') and text.endswith(']'):
            return text.count('[') == text.count(']')
        elif text.startswith('{') and text.endswith('}'):
            return text.count('{') == text.count('}')
        
        return False
    
    def _normalize_saas_ideas(self, data: List[Dict]) -> List[Dict]:
        """SaaS idea verilerini normalize et ve validate et."""
        
        if not isinstance(data, list):
            print("⚠️ [Analyzer] Data is not a list, attempting to convert...")
            if isinstance(data, dict):
                data = [data]
            else:
                return []
        
        normalized_ideas = []
        
        for i, idea in enumerate(data):
            try:
                # Zorunlu alanları kontrol et
                required_fields = ['title', 'description', 'source', 'potential', 
                                 'tags', 'validation', 'marketSize', 'painPoints']
                
                normalized_idea = {}
                
                for field in required_fields:
                    if field not in idea:
                        print(f"⚠️ [Analyzer] Missing field '{field}' in idea {i+1}")
                        continue
                    
                    # Potential alanını özel olarak handle et
                    if field == 'potential':
                        normalized_idea[field] = self._normalize_potential(idea[field])
                    elif field in ['tags', 'painPoints'] and isinstance(idea[field], str):
                        # String'i array'e çevir
                        normalized_idea[field] = [idea[field]]
                    else:
                        normalized_idea[field] = idea[field]
                
                # Tüm zorunlu alanlar varsa ekle
                if len(normalized_idea) == len(required_fields):
                    normalized_ideas.append(normalized_idea)
                else:
                    print(f"⚠️ [Analyzer] Skipping idea {i+1} due to missing fields")
                    
            except Exception as e:
                print(f"⚠️ [Analyzer] Error normalizing idea {i+1}: {e}")
                continue
        
        print(f"✅ [Analyzer] Successfully normalized {len(normalized_ideas)} ideas")
        return normalized_ideas
    
    def _normalize_potential(self, potential_value) -> int:
        """Potential değerini integer'a çevir."""
        
        if isinstance(potential_value, int):
            return max(1, min(10, potential_value))  # 1-10 arasında clamp et
        
        if isinstance(potential_value, str):
            # String'den sayısal değer çıkarmaya çalış
            potential_str = potential_value.lower()
            
            if 'high' in potential_str or 'strong' in potential_str:
                return 8
            elif 'moderate' in potential_str or 'medium' in potential_str:
                return 6
            elif 'low' in potential_str or 'weak' in potential_str:
                return 3
            else:
                # Sayı arayıp çıkarmaya çalış
                numbers = re.findall(r'\d+', potential_str)
                if numbers:
                    return max(1, min(10, int(numbers[0])))
        
        # Default değer
        return 5