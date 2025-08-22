import os, json
from core.config import AppConfig
from core.logger import get_logger

log = get_logger()

def load_job_profile(job_title: str, cfg: AppConfig) -> dict:
    # Map title to filename
    fname = job_title.lower().replace(" ", "_") + ".json"
    path = os.path.join(cfg.job_profiles_dir, fname)
    if not os.path.exists(path):
        log.warning(f"No baseline profile for {job_title}, using fallback.")
        return {"title": job_title, "core_skills": ["python","sql","statistics","machine learning"]}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def synthesize_required_skills(job_title: str, cfg: AppConfig) -> list[str]:
    base = load_job_profile(job_title, cfg)["core_skills"]
    # Optional: web enrichment + LLM summarization
    if cfg.use_llm_enrichment:
        try:
            from web_enrichment.sources import enrich_skills_from_web
            enriched = enrich_skills_from_web(job_title)
            # simple merge & dedupe
            s = set(x.lower() for x in base)
            for k in enriched:
                s.add(k.lower())
            return sorted(s)
        except Exception as e:
            log.exception("Web enrichment failed; using baseline.")
    return base
