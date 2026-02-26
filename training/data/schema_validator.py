from typing import List

import pandas as pd


class SchemaValidationError(Exception):
    """Custom exception raised when dataset schema validation fails."""


class SchemaValidator:
    """Reusable schema validation utility for datasets."""

    def __init__(self, required_columns: List[str]) -> None:
        """Initialize validator with required column names."""
        self.required_columns = required_columns

    def validate_required_columns(self, df: pd.DataFrame) -> None:
        """Ensure required columns exist in DataFrame."""
        missing_columns = [
            col for col in self.required_columns if col not in df.columns
        ]

        if missing_columns:
            raise SchemaValidationError(
                f"Missing required columns: {missing_columns}"
            )

    def validate_non_empty(self, df: pd.DataFrame) -> None:
        """Ensure DataFrame is not empty."""
        if df.empty:
            raise SchemaValidationError("Dataset is empty.")

    def validate(self, df: pd.DataFrame) -> None:
        """Run full schema validation pipeline."""
        self.validate_non_empty(df)
        self.validate_required_columns(df)