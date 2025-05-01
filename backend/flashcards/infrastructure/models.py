from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from backend.infrastructure.db.database import Base


class FlashcardModel(Base):
    __tablename__ = "flashcards"

    id = Column(String, primary_key=True, index=True)
    lemma = Column(String, index=True)
    user_id = Column(String, index=True)

    sentences = relationship("SentenceModel", back_populates="flashcard")

class SentenceModel(Base):
    __tablename__ = "sentences"

    id = Column(String, primary_key=True, index=True)
    text = Column(String, index=True)
    flashcard_id = Column(String, ForeignKey("flashcards.id"), index=True)

    flashcard = relationship("FlashcardModel", back_populates="sentences")