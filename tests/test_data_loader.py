import pandas as pd
import pytest
from pathlib import Path

from training.data.schema_validator import SchemaValidator, SchemaValidationError
from training.data.resume_loader import ResumeDataLoader
from training.data.jd_loader import JobDescriptionLoader


def test_schema_validator_missing_column() -> None:
    """Test that missing required columns raise SchemaValidationError."""
    df = pd.DataFrame({"A": [1, 2]})
    validator = SchemaValidator(required_columns=["Resume"])

    with pytest.raises(SchemaValidationError):
        validator.validate(df)


def test_schema_validator_empty_dataframe() -> None:
    """Test that empty DataFrame raises SchemaValidationError."""
    df = pd.DataFrame(columns=["Resume"])
    validator = SchemaValidator(required_columns=["Resume"])

    with pytest.raises(SchemaValidationError):
        validator.validate(df)


def test_resume_loader_success(tmp_path: Path) -> None:
    """Test successful resume loading and column standardization."""
    test_file = tmp_path / "resume.csv"

    df = pd.DataFrame(
        {
            "Resume": ["Sample resume text"],
            "Category": ["IT"],
        }
    )

    df.to_csv(test_file, index=False)

    loader = ResumeDataLoader(test_file)
    result = loader.load()

    assert "resume_text" in result.columns
    assert "category" in result.columns
    assert result.shape[0] == 1


def test_jd_loader_success(tmp_path: Path) -> None:
    """Test successful job description loading and text concatenation."""
    test_file = tmp_path / "jd.csv"

    df = pd.DataFrame(
        {
            "title": ["Engineer"],
            "description": ["Build systems"],
            "requirements": ["Python required"],
        }
    )

    df.to_csv(test_file, index=False)

    loader = JobDescriptionLoader(test_file)
    result = loader.load()

    assert "jd_text" in result.columns
    assert "title" in result.columns
    assert "Engineer" in result["jd_text"].iloc[0]
    assert result.shape[0] == 1


def test_resume_loader_missing_column(tmp_path: Path) -> None:
    """Test resume loader fails when required column is missing."""
    test_file = tmp_path / "resume_invalid.csv"

    df = pd.DataFrame(
        {
            "Resume": ["Text only"],
        }
    )

    df.to_csv(test_file, index=False)

    loader = ResumeDataLoader(test_file)

    with pytest.raises(SchemaValidationError):
        loader.load()