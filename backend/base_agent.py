# base_agent.py
import os
import httpx
import asyncio
import re
import json
from typing import Union

# Ortam değişkenlerini bu dosyada da yüklemek iyi bir pratiktir,
# çünkü bu dosya tek başına test edilebilir.
from dotenv import load_dotenv
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

class BaseAgent:
    """Ortak yetenekleri (LLM çağrısı gibi) barındıran temel agent sınıfı."""
    def __init__(self):
        self.openrouter_key = OPENROUTER_API_KEY

    async def call_llm(self, prompt: str, system_prompt: str = None, max_retries: int = 3) -> str:
        # ... call_llm fonksiyonunun tam içeriği buraya gelecek ...
        # (Önceki yanıttaki kodun aynısı)
        if not self.openrouter_key:
            print("⚠️ No OpenRouter API key, returning fallback string.")
            return '{"error": "API key not configured"}'
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(max_retries):
            try:
                print(f"🤖 LLM attempt {attempt + 1}/{max_retries}")
                payload = {
                    "model": "deepseek/deepseek-r1-0528:free",
                    "messages": messages, "temperature": 0.7, "max_tokens": 4000
                }
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers={"Authorization": f"Bearer {self.openrouter_key}", "Content-Type": "application/json"},
                        json=payload
                    )
                response.raise_for_status()
                content = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
                if not content: raise ValueError("Empty response from LLM")
                
                print("✅ LLM success")
                return content
            except Exception as e:
                print(f"❌ LLM error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    return '{"error": "LLM call failed after multiple retries"}'
                await asyncio.sleep(1)
        return '{"error": "LLM call failed"}'