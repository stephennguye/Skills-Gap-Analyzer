from loguru import logger
import sys, os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger.remove()
logger.add(sys.stderr, level="INFO", enqueue=True)
logger.add(LOG_PATH, rotation="5 MB", retention=10, level="DEBUG", enqueue=True)

def get_logger():
    return logger