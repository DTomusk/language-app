from fastapi import FastAPI
from backend.infrastructure.db.database import Base, engine
from backend.user_management.infrastructure.models import UserModel
from backend.user_management.api.routes import router as user_management_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(
    user_management_router,
    prefix="/users",
    tags=["user_management"],
)