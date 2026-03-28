from typing import Dict

from loguru import logger

from app.services.resume_parser import ResumeParser
from app.services.similarity_engine import SimilarityEngine


class SimilarityFeatureBuilder:
    """Build ML features for resume-JD matching."""

    def __init__(
        self,
        parser: ResumeParser,
        similarity_engine: SimilarityEngine,
    ) -> None:
        """Initialize feature builder."""
        self.parser = parser
        self.similarity_engine = similarity_engine

    def build_features(self, resume_text: str, jd_text: str) -> Dict[str, float]:
        """Generate feature set for a resume-JD pair."""

        logger.debug("Building similarity features")

        # Parse resume
        parsed_resume = self.parser.parse(resume_text)

        # Semantic similarity
        similarity_result = self.similarity_engine.compute_similarity(
            resume_text, jd_text
        )

        similarity_score = similarity_result["cosine_similarity"]

        # Text length features
        resume_length = len(resume_text.split())
        jd_length = len(jd_text.split())

        length_difference = abs(resume_length - jd_length)

        # Skill overlap
        resume_skills = self._flatten_skills(parsed_resume["skills"])
        jd_skills = self._extract_jd_skills(jd_text)

        overlap = resume_skills.intersection(jd_skills)

        skill_overlap_count = len(overlap)

        skill_overlap_ratio = (
            skill_overlap_count / len(jd_skills) if jd_skills else 0
        )

        # Experience
        experience_years = parsed_resume["experience_years"]

        return {
            "similarity_score": similarity_score,
            "resume_length": resume_length,
            "jd_length": jd_length,
            "length_difference": length_difference,
            "skill_overlap_count": skill_overlap_count,
            "skill_overlap_ratio": skill_overlap_ratio,
            "experience_years": experience_years,
        }

    def _flatten_skills(self, categorized_skills) -> set:
        """Convert categorized skills into flat set."""
        flat = set()
        for skills in categorized_skills.values():
            flat.update(skills)
        return flat

    def _extract_jd_skills(self, jd_text: str) -> set:
        """Basic JD skill extraction using parser logic."""
        parsed_jd = self.parser.parse(jd_text)
        return self._flatten_skills(parsed_jd["skills"])