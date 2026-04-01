import os
os.environ["THINC_NO_TORCH"] = "1"
os.environ["CUDA_VISIBLE_DEVICES"] = ""

from fastapi import FastAPI,Form
from pydantic import BaseModel
from loguru import logger
import joblib
import numpy as np
from pathlib import Path

from app.models.embedding_model import EmbeddingModel
from app.services.nlp_model import NLPModel
from app.services.resume_parser import ResumeParser
from app.services.section_detector import ResumeSectionDetector
from app.services.similarity_engine import SimilarityEngine
from training.features.similarity_features import SimilarityFeatureBuilder
from fastapi import UploadFile, File
from app.services.pdf_parser import PDFParser

# -------------------------
# Request Schema
# -------------------------
class AnalyzeRequest(BaseModel):
    resume_text: str
    job_description: str


# -------------------------
# Initialize App
# -------------------------
app = FastAPI(title="AI Resume Screening API")


# -------------------------
# Load Components (startup)
# -------------------------
logger.info("Loading models and services...")

nlp = NLPModel()
section_detector = ResumeSectionDetector()
parser = ResumeParser(nlp, section_detector)

pdf_parser = PDFParser()

embedding_model = EmbeddingModel()
similarity_engine = SimilarityEngine(embedding_model)

feature_builder = SimilarityFeatureBuilder(parser, similarity_engine)

model_dir = Path("artifacts/models")
xgb_model = joblib.load(model_dir / "xgb_model.joblib")
lgb_model = joblib.load(model_dir / "lgb_model.joblib")

logger.info("API ready.")


# -------------------------
# Endpoint
# -------------------------
@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    resume_text = request.resume_text
    jd_text = request.job_description

    # Build features
    features = feature_builder.build_features(resume_text, jd_text)
    X = np.array([list(features.values())])

    # Ensemble prediction
    xgb_prob = xgb_model.predict_proba(X)[0][1]
    lgb_prob = lgb_model.predict_proba(X)[0][1]

    prob = (xgb_prob + lgb_prob) / 2

    match_score = round(prob * 100, 2)

    # Basic explainability (simple version)
    parsed_resume = parser.parse(resume_text)

    resume_skills = set(
        skill for category in parsed_resume["skills"].values()
        for skill in category
    )

    jd_words = set(jd_text.lower().split())

    skills_matched = list(resume_skills & jd_words)
    skills_missing = list(resume_skills - jd_words)

    return {
        "match_score": match_score,
        "confidence": round(prob, 4),
        "skills_matched": skills_matched[:10],
        "skills_missing": skills_missing[:10],
    }

@app.post("/analyze-pdf")
async def analyze_pdf(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Upload PDF resume + JD → get match score
    """

    # Validate file
    if not file.filename.endswith(".pdf"):
        return {"error": "Only PDF files are supported"}

    # Extract text
    resume_text = pdf_parser.extract_text(file.file)

    # Build features
    features = feature_builder.build_features(resume_text, job_description)
    X = np.array([list(features.values())])
    
    print("---- DEBUG (FEATURES) ----")
    print("Feature names:",features)

    # Ensemble prediction
    xgb_prob = xgb_model.predict_proba(X)[0][1]
    lgb_prob = lgb_model.predict_proba(X)[0][1]

    prob = (xgb_prob + lgb_prob) / 2
    match_score = round(prob * 100, 2)

    # Parse resume for skills
    parsed_resume = parser.parse(resume_text)

    resume_skills = set(
        skill for category in parsed_resume["skills"].values()
        for skill in category
    )

    jd_words = set(job_description.lower().split())

    skills_matched = list(resume_skills & jd_words)
    skills_missing = list(resume_skills - jd_words)

    print("---- DEBUG ----")
    print("Resume length:", len(resume_text))
    print("First 200 chars:", resume_text[:200])
    print("----------------")
    
    return {
        "match_score": match_score,
        "confidence": round(prob, 4),
        "skills_matched": skills_matched[:10],
        "skills_missing": skills_missing[:10],
        "resume_preview": resume_text[:500]  # helpful debug
    }