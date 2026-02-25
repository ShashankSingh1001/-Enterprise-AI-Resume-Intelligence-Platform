from fastapi import APIRouter


router = APIRouter(prefix="/api/v1", tags=["Health"])


@router.get("/health")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok"}