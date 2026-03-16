from unittest.mock import Mock

from app.services.resume_parser import ResumeParser
from app.services.section_detector import ResumeSectionDetector


def test_resume_parser_basic():
    text = """
    Skills
    Python, Java

    Experience
    Software engineer with 5 years of experience.

    Education
    Master of Science
    """

    # Create mock tokens like spaCy tokens
    token_python = Mock()
    token_python.text = "python"

    token_java = Mock()
    token_java.text = "java"

    tokens = [token_python, token_java]

    # Mock spaCy doc
    mock_doc = Mock()
    mock_doc.__iter__ = Mock(return_value=iter(tokens))
    mock_doc.text = text.lower()
    mock_doc.sents = [Mock(text=line) for line in text.split("\n")]

    # Mock NLP model
    mock_nlp = Mock()
    mock_nlp.process.return_value = mock_doc

    section_detector = ResumeSectionDetector()

    parser = ResumeParser(
        nlp_model=mock_nlp,
        section_detector=section_detector
    )

    result = parser.parse(text)

    assert result["experience_years"] == 5
    assert result["education_level"] == "master"