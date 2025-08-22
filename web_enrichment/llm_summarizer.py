import requests, json
from core.logger import get_logger

log = get_logger()

def summarize_skills_with_ollama(texts: list[str], model="llama3"):
    prompt = """Extract a concise bullet list of skills required for the role based on the following texts. 
Return as a JSON array of strings (unique, lowercased). Texts:
"""
    content = prompt + "\n\n".join(texts[:3])
    r = requests.post("http://localhost:11434/api/generate", json={"model": model, "prompt": content, "stream": False}, timeout=120)
    r.raise_for_status()
    out = r.json().get("response","[]")
    try:
        skills = json.loads(out)
        return sorted(set([s.strip().lower() for s in skills if isinstance(s, str)]))
    except Exception:
        log.warning("LLM output not JSON; skipping.")
        return []
