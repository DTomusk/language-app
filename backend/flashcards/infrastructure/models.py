from sqlalchemy import Column, String
from backend.infrastructure.db.database import Base


class FlashcardModel(Base):
    __tablename__ = "flashcards"

    id = Column(String, primary_key=True, index=True)
    lemma = Column(String, index=True)
    user_id = Column(String, index=True)