from infrastructure.db.database import Base, engine
from user_management.infrastructure.models import UserModel

Base.metadata.create_all(bind=engine)