from pathlib import Path
from typing import Any, Dict

import yaml
from pydantic import BaseModel


class DatasetConfig(BaseModel):
    """Dataset configuration schema."""

    directory: str
    filename: str


class DataSettings(BaseModel):
    """Training data settings loaded from YAML."""

    resume_dataset: DatasetConfig
    jd_dataset: DatasetConfig

    @staticmethod
    def _detect_project_root() -> Path:
        """Detect project root by locating pyproject.toml."""
        current = Path(__file__).resolve()

        for parent in current.parents:
            if (parent / "pyproject.toml").exists():
                return parent

        raise FileNotFoundError("Could not locate project root.")

    @classmethod
    def load(cls, config_path: Path = Path("configs/data.yaml")) -> "DataSettings":
        """Load YAML configuration and return validated settings."""
        project_root = cls._detect_project_root()
        full_config_path = project_root / config_path

        if not full_config_path.exists():
            raise FileNotFoundError(f"Config file not found: {full_config_path}")

        with open(full_config_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f)

        return cls(**data)

    def get_resume_path(self) -> Path:
        """Return absolute path to resume dataset."""
        root = self._detect_project_root()
        return (root / self.resume_dataset.directory / self.resume_dataset.filename).resolve()

    def get_jd_path(self) -> Path:
        """Return absolute path to job description dataset."""
        root = self._detect_project_root()
        return (root / self.jd_dataset.directory / self.jd_dataset.filename).resolve()