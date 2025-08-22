import json, re
from collections import Counter
from core.logger import get_logger
from core.config import AppConfig

log = get_logger()

def load_taxonomy(cfg: AppConfig) -> dict:
    with open(cfg.skills_taxonomy_path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[^a-z0-9+#.\-\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def extract_skills(text: str, taxonomy: dict, extra_terms: list[str] | None = None) -> dict:
    """
    Return dict {skill: count} for all taxonomy terms found in text
    Also optionally scan extra_terms 
    """
    nt = normalize(text)
    counts = Counter()

    # taxonomy terms
    for group, terms in taxonomy.items():
        for term in terms:
            pattern = r"(?<![a-z0-9+.#-])" + re.escape(term.lower()) + r"(?![a-z0-9+.#-])"
            matches = re.findall(pattern, nt)
            if matches:
                counts[term] += len(matches)

    # extra terms (job profile skills)
    if extra_terms:
        for term in extra_terms:
            term_l = (term or "").strip().lower()
            if not term_l:
                continue
            pattern = r"(?<![a-z0-9+.#-])" + re.escape(term_l) + r"(?![a-z0-9+.#-])"
            matches = re.findall(pattern, nt)
            if matches:
                counts[term_l] += len(matches)

    log.info(f"Extracted {len(counts)} skills from resume (taxonomy + extras)")
    return dict(counts)
