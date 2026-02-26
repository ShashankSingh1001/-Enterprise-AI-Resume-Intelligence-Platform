from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from training.data.schema_validator import SchemaValidator, SchemaValidationError


class ResumeDataLoader:
    """Loader for resume dataset."""

    REQUIRED_COLUMNS = ["Resume", "Category"]

    def __init__(self, file_path: Path) -> None:
        """Initialize loader with dataset file path."""
        self.file_path = file_path
        self.validator = SchemaValidator(self.REQUIRED_COLUMNS)

    def load(self) -> pd.DataFrame:
        """Load and validate resume dataset."""
        logger.info(f"Loading resume dataset from {self.file_path}")

        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")

        df = pd.read_csv(self.file_path)

        self.validator.validate(df)

        df = self._basic_cleaning(df)

        logger.info(f"Loaded {len(df)} resumes successfully")

        return df

    def _basic_cleaning(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform basic cleaning and standardization."""
        df = df.copy()

        df["Resume"] = df["Resume"].fillna("").astype(str)
        df["Category"] = df["Category"].fillna("Unknown").astype(str)

        df = df.rename(
            columns={
                "Resume": "resume_text",
                "Category": "category",
            }
        )

        df = df[["resume_text", "category"]]

        return df