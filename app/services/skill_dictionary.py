from typing import Dict, Set


class SkillDictionary:
    """Centralized categorized IT skill dictionary."""

    def __init__(self) -> None:
        """Initialize categorized skill sets."""
        self.skill_categories: Dict[str, Set[str]] = self._build_skill_categories()
        self.skill_lookup: Dict[str, str] = self._build_lookup()

    def _build_skill_categories(self) -> Dict[str, Set[str]]:
        """Define categorized skills."""
        return {
            "programming_languages": {
                "python", "java", "c++", "c", "c#", "javascript",
                "typescript", "go", "golang", "rust", "kotlin",
                "swift", "php", "ruby", "r", "scala"
            },
            "web_frameworks": {
                "django", "flask", "fastapi", "spring", "spring boot",
                "node.js", "express", "react", "angular", "vue",
                "next.js", "asp.net"
            },
            "databases": {
                "mysql", "postgresql", "mongodb", "sqlite",
                "oracle", "redis", "cassandra", "dynamodb"
            },
            "cloud_devops": {
                "aws", "azure", "gcp", "google cloud",
                "docker", "kubernetes", "terraform",
                "jenkins", "ci/cd", "git", "github", "gitlab",
                "linux", "bash"
            },
            "data_ml": {
                "machine learning", "deep learning", "nlp",
                "pandas", "numpy", "scikit-learn",
                "tensorflow", "pytorch", "xgboost",
                "lightgbm", "mlflow"
            },
            "big_data": {
                "hadoop", "spark", "kafka", "airflow"
            },
            "visualization": {
                "power bi", "tableau"
            },
            "architecture": {
                "microservices", "rest api", "graphql"
            }
        }

    def _build_lookup(self) -> Dict[str, str]:
        """Create reverse lookup from skill to category."""
        lookup: Dict[str, str] = {}
        for category, skills in self.skill_categories.items():
            for skill in skills:
                lookup[skill] = category
        return lookup

    def get_categories(self) -> Dict[str, Set[str]]:
        """Return skill categories."""
        return self.skill_categories

    def get_lookup(self) -> Dict[str, str]:
        """Return skill-to-category mapping."""
        return self.skill_lookup