from fastapi import APIRouter
from .register_route import router as register_router
from .oauth import router as oauth_router
from .login_route import router as login_router
from .delete_user import router as delete_user_router
from .user_update import router as  user_update_router


# Crear un router combinado
router = APIRouter()
router.include_router(register_router)
router.include_router(oauth_router)
router.include_router(login_router)
router.include_router(delete_user_router)
router.include_router(user_update_router)

__all__ = ["router"] 
