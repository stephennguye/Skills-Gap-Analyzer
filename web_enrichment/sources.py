from duckduckgo_search import DDGS
import trafilatura, time
from core.logger import get_logger
from core.exceptions import CrawlError

log = get_logger()

def _fetch_articles(query: str, max_n: int = 8):
    try:
        with DDGS() as ddgs:
            hits = list(ddgs.text(query, max_results=max_n, region="wt-wt", safesearch="moderate"))
        urls = [h["href"] for h in hits if "href" in h]
        return urls
    except Exception as e:
        log.exception("Search failed")
        raise CrawlError(str(e)) from e

def _extract_text(url: str) -> str:
    try:
        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            return ""
        return trafilatura.extract(downloaded) or ""
    except Exception:
        return ""

def enrich_skills_from_web(job_title: str) -> list[str]:
    q = f"{job_title} required skills site:blog or site:careers or site:medium.com"
    urls = _fetch_articles(q, max_n=6)
    corpus = []
    for u in urls:
        time.sleep(0.5)
        txt = _extract_text(u)
        if txt:
            corpus.append(txt)
    # simple heuristic extraction (you can LLM summarize next)
    keywords = set()
    seeds = ["python","sql","statistics","machine learning","cloud","aws","azure","gcp","tensorflow","pytorch","docker","kubernetes","spark","airflow","mlops","tableau","power bi","feature engineering","nlp","computer vision","experiment design","causal inference"]
    for c in corpus:
        lc = c.lower()
        for k in seeds:
            if k in lc:
                keywords.add(k)
    return sorted(keywords)
