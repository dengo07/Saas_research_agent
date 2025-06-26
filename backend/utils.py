import json
import ast

def safe_string_to_dict(s: str) -> dict:
    """
    Bir metni güvenli bir şekilde Python sözlüğüne dönüştürür.
    Önce JSON olarak dener, başarısız olursa ast.literal_eval kullanır.
    """
    if not isinstance(s, str):
        # Eğer zaten metin değilse (belki zaten dict'tir), dokunma
        return s
    
    # Metin içindeki olası ```json ... ``` bloklarını temizle
    if s.strip().startswith("```json"):
        s = s.strip()[7:-3].strip()
    elif s.strip().startswith("```"):
        s = s.strip()[3:-3].strip()

    try:
        # Standart JSON formatını dene
        return json.loads(s)
    except json.JSONDecodeError:
        try:
            # Python'un kendi sözlük/liste/tuple yapısını (tek tırnak vb. kabul eder) dene
            # Bu, eval() kadar tehlikeli değildir.
            return ast.literal_eval(s)
        except (ValueError, SyntaxError, MemoryError, TypeError):
            # Her iki yöntem de başarısız olursa, hatayı önlemek için boş bir sözlük döndür
            # veya bir log kaydı bırakabilirsiniz.
            print(f"UYARI: Metin sözlüğe dönüştürülemedi: {s}")
            return {}