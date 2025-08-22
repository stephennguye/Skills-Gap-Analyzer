from sentence_transformers import SentenceTransformer
from core.exceptions import EmbeddingError
from core.logger import get_logger

log = get_logger()
_model_cache = {}

def get_model(name: str) -> SentenceTransformer:
    if name not in _model_cache:
        log.info(f"Loading embedding model: {name}")
        _model_cache[name] = SentenceTransformer(name)
    return _model_cache[name]

def embed(texts, model_name: str):
    try:
        m = get_model(model_name)
        return m.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    except Exception as e:
        log.exception("Embedding failed")
        raise EmbeddingError(str(e)) from e
