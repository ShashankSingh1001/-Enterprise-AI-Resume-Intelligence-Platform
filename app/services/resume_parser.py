from pydoc import doc
import re
from collections import defaultdict
from typing import Dict, List, Set,Any

from loguru import logger

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.services.nlp_model import NLPModel
from app.services.skill_dictionary import SkillDictionary
from app.services.section_detector import ResumeSectionDetector

class ResumeParser:
    """Parses resume text and extracts structured information."""

    EDUCATION_KEYWORDS = {
        "bachelor": "bachelor",
        "b.tech": "bachelor",
        "btech": "bachelor",
        "bsc": "bachelor",
        "master": "master",
        "m.tech": "master",
        "mtech": "master",
        "msc": "master",
        "phd": "phd",
        "doctorate": "phd",
    }

    EXPERIENCE_PATTERN = re.compile(r"(\d+)\s*\+?\s*(years?|yrs?)", re.IGNORECASE)

    def __init__(self, nlp_model:"NLPModel",section_detector:ResumeSectionDetector) -> None:
        """Initialize parser with injected NLP model."""
        self.nlp_model = nlp_model
        self.section_detector = section_detector

        self.skill_dict = SkillDictionary()
        self.skill_categories = self.skill_dict.get_categories()
        self.skill_lookup = self.skill_dict.get_lookup()

    def parse(self, text: str) -> Dict[str, any]:
        """Parse resume text and return structured information."""
        logger.debug("Parsing resume text")
        sections = self.section_detector.detect_sections(text)

        doc = self.nlp_model.process(text.lower())

        categorized_skills, skill_frequency = self._extract_skills(doc)

        experience_text = sections.get("experience",text)
        experience_years = self._extract_experience(experience_text)

        education_text = sections.get("education",text)
        education_level = self._extract_education(education_text)

        return {
            "skills": categorized_skills,
            "skill_frequency": skill_frequency,
            "experience_years": experience_years,
            "education_level": education_level,
            "sections_detected": list(sections.keys())
        }

    def _extract_skills(
        self, doc:Any
    ) -> (Dict[str, List[str]], Dict[str, int]):  # type: ignore
        """Extract categorized skills with frequency scoring."""
        categorized_skills: Dict[str, Set[str]] = defaultdict(set)
        skill_frequency: Dict[str, int] = defaultdict(int)

        tokens = [token.text for token in doc]

        # Token-level matching
        for token in tokens:
            if token in self.skill_lookup:
                category = self.skill_lookup[token]
                categorized_skills[category].add(token)
                skill_frequency[token] += 1

        # Phrase-level matching for multi-word skills
        text = doc.text
        for skill in self.skill_lookup.keys():
            if " " in skill and skill in text:
                category = self.skill_lookup[skill]
                categorized_skills[category].add(skill)
                skill_frequency[skill] += text.count(skill)

        # Convert sets to sorted lists
        categorized_skills_final = {
            category: sorted(list(skills))
            for category, skills in categorized_skills.items()
        }

        return categorized_skills_final, dict(skill_frequency)

    def _extract_experience(self, text: str) -> int:
        """Extract total years of experience using regex."""
        doc = self.nlp_model.process(text.lower())
        experience_keywords = {
        "experience",
        "worked",
        "working",
        "developer",
        "engineer",
        "professional",
        "career",
        "employment",
        }
        years_found = []

        for sent in doc.sents:
            sentence_text = sent.text

            # Check if sentence contains experience-related context
            if any(keyword in sentence_text for keyword in experience_keywords):

                matches = self.EXPERIENCE_PATTERN.findall(sentence_text)

                for match in matches:
                    if match[0].isdigit():
                        years_found.append(int(match[0]))

        return max(years_found) if years_found else 0


    def _extract_education(self, text: str) -> str:
        """Detect highest education level."""
        text_lower = text.lower()
        detected_levels: Set[str] = set()

        for keyword, level in self.EDUCATION_KEYWORDS.items():
            if keyword in text_lower:
                detected_levels.add(level)

        if "phd" in detected_levels:
            return "phd"
        if "master" in detected_levels:
            return "master"
        if "bachelor" in detected_levels:
            return "bachelor"

        return "unknown"