import re
from typing import Dict


class ResumeSectionDetector:
    """Detects common resume sections."""

    SECTION_PATTERNS = {
        "skills": r"(technical skills|skills|core competencies)",
        "experience": r"(work experience|professional experience|experience)",
        "education": r"(education|academic background)",
        "projects": r"(projects|project experience)",
        "certifications": r"(certifications|licenses)"
    }

    def detect_sections(self, text: str) -> Dict[str, str]:
        """Split resume text into logical sections."""
        sections: Dict[str, str] = {}

        lines = text.split("\n")

        current_section = "general"
        sections[current_section] = []

        for line in lines:
            lower_line = line.lower()

            matched = False

            for section, pattern in self.SECTION_PATTERNS.items():
                if re.search(pattern, lower_line):
                    current_section = section
                    sections[current_section] = []
                    matched = True
                    break

            if not matched:
                sections[current_section].append(line)

        return {
            section: "\n".join(content)
            for section, content in sections.items()
        }