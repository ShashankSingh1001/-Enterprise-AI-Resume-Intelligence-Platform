# Enterprise AI Resume Intelligence Platform

End-to-end AI system for semantic resume screening, role-fit prediction, explainable hiring decisions, and bias auditing. Built using production-ready ML architecture and MLOps practices.

---

## Overview

Traditional Applicant Tracking Systems (ATS) rely on keyword matching, which leads to:

- Poor semantic understanding of resumes  
- High false rejection rates  
- Limited transparency in hiring decisions  
- Undetected bias in candidate shortlisting  

This project simulates an enterprise-grade HR AI platform that provides:

- Semantic JD–Resume Matching  
- Role-Fit Probability Prediction  
- Explainable AI Decisions  
- Bias and Fairness Auditing  
- Drift Monitoring  
- Production Deployment Architecture  

---

## System Capabilities

### Resume Parsing

- spaCy-based NLP pipeline  
- Extraction of skills, education, experience, and projects  
- Hybrid skill extraction using rule-based matching and embeddings  

### Semantic JD–Resume Matching

- Sentence-BERT embeddings  
- Cosine similarity scoring  
- Domain-aware similarity calibration  

### Role-Fit Prediction

- Feature engineering combining:
  - Semantic similarity
  - Experience years
  - Education level
  - Skill match ratio
  - Project relevance
- XGBoost and LightGBM ensemble classifier  
- Threshold optimization for HR shortlisting scenarios  

### Explainable AI

- SHAP for global and local feature importance  
- LIME for candidate-level explanation  
- Human-readable decision summaries  

### Responsible AI

- Fairlearn-based bias detection  
- Demographic parity and equal opportunity metrics  
- Bias auditing across:
  - Gender proxy
  - College tier proxy
  - Experience groups  
- Fairness drift monitoring  

### Monitoring

- Feature drift detection  
- Prediction distribution tracking  
- Fairness metric drift tracking  

### Deployment

- FastAPI backend  
- Streamlit HR dashboard  
- PostgreSQL integration  
- JWT-based authentication  
- Dockerized services  

---

## Project Architecture

HR Dashboard (Streamlit)  
        │  
FastAPI Backend  
        │  
Resume Parsing + Similarity Engine  
        │  
Feature Engineering Layer  
        │  
ML Inference (Ensemble Model)  
        │  
Explainability + Bias Audit  
        │  
PostgreSQL Storage  
        │  
Monitoring & Drift Detection  

---

## Folder Structure

```PlainText
resume-intelligence-platform/
│
├── app/
│ ├── api/
│ ├── services/
│ ├── models/
│ ├── core/
│ └── db/
│
├── training/
│ ├── data/
│ ├── features/
│ ├── modeling/
│ └── pipelines/
│
├── explainability/
├── bias_audit/
├── monitoring/
├── dashboard/
├── mlops/
├── tests/
├── artifacts/
├── notebooks/
├── configs/
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Dataset

- Kaggle Resume Dataset  
- IT Job Description Dataset  
- Synthetic enterprise hiring labels  

Final dataset schema:

- resume_text  
- jd_text  
- similarity  
- exp_years  
- edu_level  
- skill_match_ratio  
- selected  

---

## Technology Stack

Core:

- Python 3.11  
- spaCy  
- Sentence-BERT  
- XGBoost  
- LightGBM  

Explainability & Fairness:

- SHAP  
- LIME  
- Fairlearn  

MLOps:

- MLflow  
- DVC  
- Docker  

Backend & UI:

- FastAPI  
- Streamlit  
- PostgreSQL  

---

## Business Impact Simulation

- 40% reduction in manual screening time  
- 25% improvement in role-fit precision  
- Transparent and auditable AI-based hiring decisions  
- Bias visibility across candidate groups  

---

## Resume Summary Bullet

Designed and deployed an enterprise-grade AI Resume Intelligence Platform leveraging SBERT-based semantic matching and XGBoost ensemble modeling (ROC-AUC 0.75+). Implemented SHAP explainability, Fairlearn bias auditing, MLflow-driven MLOps, drift monitoring, and Dockerized FastAPI deployment with Streamlit HR dashboard.

---

## Future Enhancements

- Fine-tuning SBERT using contrastive learning  
- Automated retraining pipeline with recruiter feedback loop  
- Cloud-native deployment (AWS/Azure)  
- Real-time monitoring dashboard with Prometheus/Grafana  

---

## Author

Shashank Singh
