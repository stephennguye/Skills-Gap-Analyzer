import os
from pydantic import BaseModel, Field

ROOT = os.path.dirname(os.path.dirname(__file__))

class AppConfig(BaseModel):
    model_name: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    skills_taxonomy_path: str = Field(default=os.path.join(ROOT, "jobs", "taxonomies", "skills_taxonomy.json"))
    job_profiles_dir: str = Field(default=os.path.join(ROOT, "data", "job_profiles"))
    course_csv_path: str = Field(default=os.path.join(ROOT, "data", "courses_sample.csv"))
    cache_dir: str = Field(default=os.path.join(ROOT, "cache"))
    use_llm_enrichment: bool = Field(default=False)  
