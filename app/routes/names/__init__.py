from fastapi import APIRouter

from routes.names.api import router as names_router


router = APIRouter()

router.include_router(
    names_router,
)
