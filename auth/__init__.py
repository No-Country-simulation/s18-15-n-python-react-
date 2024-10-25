from fastapi import APIRouter
from .register_route import router as register_router
from .oauth import router as oauth_router
from .login_route import router as login_router
from .delete_user import router as delete_user

# Crear un router combinado
router = APIRouter()
router.include_router(register_router)
router.include_router(oauth_router)
router.include_router(login_router)
router.include_router(delete_user)

__all__ = ["router"] 
