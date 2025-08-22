import pandas as pd
from nlp.embeddings import embed
from sklearn.metrics.pairwise import cosine_similarity
from core.config import AppConfig
from core.logger import get_logger

log = get_logger()

def load_courses(cfg: AppConfig):
    df = pd.read_csv(cfg.course_csv_path)
    df["skills"] = df["skills"].fillna("").astype(str)
    df["text"] = df[["title","skills","provider"]].astype(str).agg(" - ".join, axis=1)
    return df

def recommend_courses(missing_skills: list[str], cfg: AppConfig, top_k: int = 8):
    df = load_courses(cfg)
    if not len(df): return df
    q = ", ".join(missing_skills) if missing_skills else "data science machine learning"
    q_vec = embed([q], cfg.model_name)
    c_vecs = embed(df["text"].tolist(), cfg.model_name)
    sims = cosine_similarity(q_vec, c_vecs).flatten()
    df = df.copy()
    df["similarity"] = sims
    df = df.sort_values("similarity", ascending=False).head(top_k)
    log.info(f"Recommended {len(df)} courses for gaps: {missing_skills}")
    return df[["provider","title","url","skills","tier","similarity"]]
