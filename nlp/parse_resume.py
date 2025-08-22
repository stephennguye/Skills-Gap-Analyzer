import pdfplumber, docx, io
from core.exceptions import ParseError
from core.logger import get_logger

log = get_logger()

def extract_text(file_bytes: bytes, filename: str) -> str:
    try:
        if filename.lower().endswith(".pdf"):
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
            text = "\n".join(pages)
        elif filename.lower().endswith((".docx", ".doc")):
            doc = docx.Document(io.BytesIO(file_bytes))
            text = "\n".join(p.text for p in doc.paragraphs)
        else:
            # treat as plain text
            text = file_bytes.decode("utf-8", errors="ignore")
        text = " ".join(text.split())
        log.info(f"Parsed resume: {len(text)} chars")
        if len(text) < 100:
            log.warning("Resume text seems short.")
        return text
    except Exception as e:
        log.exception("Failed to parse resume")
        raise ParseError(str(e)) from e
