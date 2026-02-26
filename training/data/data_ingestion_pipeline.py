from pathlib import Path
from typing import Tuple

import pandas as pd
from loguru import logger

from training.data.resume_loader import ResumeDataLoader
from training.data.jd_loader import JobDescriptionLoader


class DataIngestionPipeline:
    """Orchestrates dataset loading and validation."""

    def __init__(
        self,
        resume_path: Path,
        jd_path: Path,
    ) -> None:
        """Initialize ingestion pipeline with dataset paths."""
        self.resume_loader = ResumeDataLoader(resume_path)
        self.jd_loader = JobDescriptionLoader(jd_path)

    def run(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Execute full data ingestion pipeline."""
        logger.info("Starting data ingestion pipeline")

        resumes_df = self.resume_loader.load()
        jd_df = self.jd_loader.load()

        self._log_summary(resumes_df, jd_df)

        logger.info("Data ingestion pipeline completed successfully")

        return resumes_df, jd_df

    def _log_summary(
        self,
        resumes_df: pd.DataFrame,
        jd_df: pd.DataFrame,
    ) -> None:
        """Log dataset summary statistics."""
        logger.info(f"Total resumes loaded: {len(resumes_df)}")
        logger.info(f"Total job descriptions loaded: {len(jd_df)}")

        logger.debug(
            f"Resume columns: {list(resumes_df.columns)}"
        )
        logger.debug(
            f"Job description columns: {list(jd_df.columns)}"
        )