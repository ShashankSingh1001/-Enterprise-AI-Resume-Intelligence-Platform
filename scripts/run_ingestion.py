from loguru import logger

from training.config.data_settings import DataSettings
from training.data.data_ingestion_pipeline import DataIngestionPipeline


def main() -> None:
    """Execute ingestion pipeline using structured configuration."""

    settings = DataSettings.load()

    resume_path = settings.get_resume_path()
    jd_path = settings.get_jd_path()

    pipeline = DataIngestionPipeline(
        resume_path=resume_path,
        jd_path=jd_path,
    )

    resumes_df, jd_df = pipeline.run()

    logger.info(f"Resumes shape: {resumes_df.shape}")
    logger.info(f"Job descriptions shape: {jd_df.shape}")


if __name__ == "__main__":
    main()