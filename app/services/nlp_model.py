from typing import Any

import spacy
from loguru import logger
from spacy.language import Language


class NLPModel:
    """Wrapper around spaCy language model."""

    def __init__(self, model_name: str = "en_core_web_sm") -> None:
        """Initialize NLP model."""
        self.model_name = model_name
        self._nlp: Language = self._load_model()

    def _load_model(self) -> Language:
        """Load spaCy model safely."""
        try:
            logger.info(f"Loading spaCy model: {self.model_name}")
            nlp = spacy.load(self.model_name)
            logger.info("spaCy model loaded successfully")
            return nlp
        except OSError as e:
            logger.error(
                f"spaCy model '{self.model_name}' not found. "
                "Install it before running NLP features."
            )
            raise e

    def process(self, text: str) -> Any:
        """Process text using spaCy pipeline."""
        return self._nlp(text)