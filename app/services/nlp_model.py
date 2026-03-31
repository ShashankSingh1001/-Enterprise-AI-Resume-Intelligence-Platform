from typing import Any

from loguru import logger

from loguru import logger


class NLPModel:
    """spaCy NLP wrapper with lazy loading."""

    def __init__(self, model_name: str = "en_core_web_sm"):
        self.model_name = model_name
        self._nlp = None

    def _load_model(self):
        """Lazy load spaCy model."""
        if self._nlp is None:
            logger.info(f"Loading spaCy model: {self.model_name}")

            import spacy  # ✅ ONLY place spaCy is imported

            self._nlp = spacy.load(self.model_name)

            logger.info("spaCy model loaded successfully")

        return self._nlp

    def process(self, text: str):
        """Process text."""
        nlp = self._load_model()
        return nlp(text)