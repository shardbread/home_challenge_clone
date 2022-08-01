from fastapi import APIRouter

from routes.folders.api import router as folders_router


router = APIRouter()

router.include_router(
    folders_router,
)
