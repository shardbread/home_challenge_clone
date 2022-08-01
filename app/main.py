from fastapi import FastAPI

from config import get_swagger_settings
from db.session import DbSessionProvider
from routes import folders, names


def get_application() -> FastAPI:
    """
        Initialize and return FastAPI instance
    :return: FastAPI instance
    """
    # configure swagger settings
    app_settings = get_swagger_settings()

    # Initialize FastAPI
    app_instance = FastAPI(**app_settings)

    @app_instance.on_event("startup")
    def startup_event():
        DbSessionProvider.setup()

    @app_instance.on_event("shutdown")
    async def shutdown_event():
        await DbSessionProvider.teardown()

    # Add api routes
    app_instance.include_router(folders.router, tags=["Folders"], prefix='/api')
    app_instance.include_router(names.router, tags=["Grouping names"], prefix='/api')

    return app_instance


app = get_application()
