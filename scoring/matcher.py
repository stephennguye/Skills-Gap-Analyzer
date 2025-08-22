import re
import numpy as np
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity
from nlp.embeddings import embed
from core.config import AppConfig

def _normalize_text(t: str) -> str:
    t = t.lower()
    t = re.sub(r"[^a-z0-9+#.\-\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()

def _split_units(text: str) -> List[str]:
    # Split into smaller units (sentences/bullets/lines) to avoid dilution
    raw = re.split(r"(?:\n|•|\u2022|;|\.)(?=\s+|$)", text)
    units = [u.strip() for u in raw if 10 <= len(u) <= 400]
    return units or [text[:4000]]

def _aliases_for(skill: str) -> List[str]:
    s = skill.lower().strip()
    alias_map = {
        "data visualization": [
            "data visualization", "visualization", "data viz",
            "dashboarding", "dashboards", "charting", "charts",
            "plotting", "plots"
        ],
        "machine learning": ["machine learning", "ml"],
        "natural language processing": ["natural language processing", "nlp"],
        "version control": ["version control", "git"],
    }
    return list(dict.fromkeys([s] + alias_map.get(s, [])))

def skill_match_scores(resume_text: str, required_skills: List[str], cfg: AppConfig) -> Dict[str, float]:
    units = _split_units(resume_text)
    resume_norm = _normalize_text(resume_text)

    # Precompute resume unit embeddings once
    unit_vecs = embed(units, cfg.model_name)

    scores: Dict[str, float] = {}
    for skill in required_skills:
        aliases = _aliases_for(skill)

        # Lexical fast-path: exact word-boundary hit for any alias
        lex_hit = False
        for a in aliases:
            pat = r"(?<![a-z0-9+.#-])" + re.escape(a) + r"(?![a-z0-9+.#-])"
            if re.search(pat, resume_norm):
                lex_hit = True
                break

        # Semantic: max cosine between any alias and any resume unit
        alias_vecs = embed(aliases, cfg.model_name)
        sims = cosine_similarity(alias_vecs, unit_vecs) if len(aliases) and len(units) else np.array([[0.0]])
        max_sim = float(np.max(sims)) if sims.size else 0.0

        # Properly map cosine [-1,1] -> [0,1]
        sem_score = (max_sim + 1.0) / 2.0

        # Combine: lexical hit guarantees a strong score; otherwise use semantic
        score = max(sem_score, 0.85) if lex_hit else sem_score

        # Clamp to [0,1]
        scores[skill] = float(max(0.0, min(1.0, score)))

    return scores

def overall_match(scores: dict) -> float:
    if not scores:
        return 0.0
    return float(np.mean(list(scores.values())))
