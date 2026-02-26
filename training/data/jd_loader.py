from pathlib import Path

import pandas as pd
from loguru import logger

from training.data.schema_validator import SchemaValidator


class JobDescriptionLoader:
    """Loader for job description dataset."""

    REQUIRED_COLUMNS = ["title", "description", "requirements"]

    def __init__(self, file_path: Path) -> None:
        """Initialize loader with dataset file path."""
        self.file_path = file_path
        self.validator = SchemaValidator(self.REQUIRED_COLUMNS)

    def load(self) -> pd.DataFrame:
        """Load and validate job description dataset."""
        logger.info(f"Loading job description dataset from {self.file_path}")

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        df = pd.read_csv(self.file_path)

        self.validator.validate(df)

        df = self._basic_cleaning(df)

        logger.info(f"Loaded {len(df)} job descriptions successfully")

        return df

    def _basic_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform basic cleaning and construct jd_text."""
        df = df.copy()

        df["title"] = df["title"].fillna("").astype(str)
        df["description"] = df["description"].fillna("").astype(str)
        df["requirements"] = df["requirements"].fillna("").astype(str)

        df["jd_text"] = (
            df["title"] + " " +
            df["description"] + " " +
            df["requirements"]
        ).str.strip()

        df = df[["jd_text", "title"]]

        return df