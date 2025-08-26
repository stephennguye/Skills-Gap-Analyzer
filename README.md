# AI Skills Gap Analyzer  
An early prototype that **analyzes a resume against a chosen job role** and highlights:  
- **Match percentage score**  
- **Missing required & nice-to-have skills**  
- **Recommended courses/resources**  

---

## Why This Matters  
Today’s job market changes quickly, and students often don’t know what skills they’re missing for a target career. This tool shows how AI can **bridge the gap between education and industry needs** by automatically:  
1. Extracting skills from a resume  
2. Comparing them to curated job role templates  
3. Prioritizing what to learn next  

---

## Current Prototype  
You paste **resume text** 

You select **target job role** 

You click **Analyze**  

You get:  
  - A **percentage fit score**  
  - A list of **missing skills**  
  - A **learning plan with resources**  
Example:  
> *Resume vs. Data Analyst* → **68% fit** → Missing *SQL, Tableau, Statistics* → Suggested resources linked.  

---

## Tech Stack Overview

### Current Stack
- **Frontend**: [Streamlit 1.38.0](https://streamlit.io/) for rapid UI prototyping and interactive dashboards.  
- **Core Libraries**:
  - **NLP & Embeddings**: `spaCy 3.7.4`, `sentence-transformers 3.0.1` for text processing and semantic similarity.
  - **Matching & Scoring**: `scikit-learn 1.5.1`, `numpy 1.26.4`, `pandas 2.2.2` for vector similarity, scoring algorithms, and structured data management.
  - **Document Parsing**: `pdfplumber 0.11.4`, `python-docx 1.1.2`, `trafilatura 1.9.0` for extraction from PDFs, DOCX files, and HTML sources.
  - **Logging & Utilities**: `loguru 0.7.2`, `tqdm 4.66.4`, `requests 2.32.3`, `joblib 1.4.2` for logging, progress tracking, API interaction, and caching.
- **Visualization**: `plotly 5.23.0` for dynamic visual insights.

### Strengths
- Modular and lightweight architecture for easy scaling.
- Robust NLP pipeline enabling semantic job-skill matching.
- Supports multiple data formats (PDF, DOCX,...).
- Clear visual representation of skill gap analysis.

### Future Enhancements
- **LLM Integration**: Utilize Large Language Models for deeper context-aware matching and skill inference.  
- **RAG (Retrieval-Augmented Generation)**: Integrate external knowledge sources (ESCO, O*NET) to enhance career insights.  
- **AI Career Agent**: Interactive AI assistant for skill gap detection, training recommendations, and personalized career guidance.  
- **Enhanced Matching Algorithm**: Hybrid scoring combining semantic, keyword-based, and contextual relevance for improved accuracy.

---




