from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.infrastructure.db.database import Base, engine
from backend.user_management.api.routes import router as user_management_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)}
    )

app.include_router(
    user_management_router,
    prefix="/users",
    tags=["user_management"],
)