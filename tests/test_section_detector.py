from app.services.section_detector import ResumeSectionDetector


def test_section_detection():
    text = """
    Skills
    Python, Java

    Experience
    Worked for 5 years as a developer.

    Education
    Bachelor of Technology
    """

    detector = ResumeSectionDetector()

    sections = detector.detect_sections(text)

    assert "skills" in sections
    assert "experience" in sections
    assert "education" in sections