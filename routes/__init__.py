from fastapi import APIRouter

from .task_routes import router as task_router


router = APIRouter()
router.include_router(task_router)

__all__ = ["router"]
