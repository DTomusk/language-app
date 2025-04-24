from sqlalchemy.orm import Session

from backend.user_management.application.repositories.user_repository import UserRepository
from backend.user_management.domain.models import User
from backend.user_management.infrastructure.models import UserModel


class SqliteUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
    
    def get_by_email(self, email: str):
        result = self.session.query(UserModel).filter_by(email=email).first()
        if result: 
            return User(
                id=result.id,
                email=result.email,
                hashed_password=result.hashed_password,
            )
        return None
    
    def save(self, user: User):
        db_user = UserModel(
            id=str(user.id),
            email=user.email.email,
            hashed_password=user.hashed_password,
        )
        self.session.add(db_user)
        self.session.commit()