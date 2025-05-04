from fastapi import Depends

from backend.flashcards.application.use_cases.add_flashcard import AddFlashcard
from backend.flashcards.application.use_cases.add_sentence_to_flashcard import AddSentenceToFlashcard
from backend.flashcards.infrastructure.repositories.sqlite_flashcard_repository import SqliteFlashcardRepository
from backend.infrastructure.db.database import get_db


def get_flashcard_repository(db=Depends(get_db)):
    return SqliteFlashcardRepository(session=db)

def add_flashcard_use_case(flashcard_repository=Depends(get_flashcard_repository)):
    return AddFlashcard(
        flashcard_repository=flashcard_repository
    )

def add_sentence_use_case(flashcard_repository=Depends(get_flashcard_repository)):
    return AddSentenceToFlashcard(
        flashcard_repository=flashcard_repository
    )