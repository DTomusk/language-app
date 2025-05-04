from fastapi import APIRouter, Depends

from backend.auth import get_current_user
from backend.flashcards.api.dependencies import add_flashcard_use_case, add_sentence_use_case

router = APIRouter()

@router.post("/{lemma}")
async def create_flashcard(lemma: str, add_flashcard_use_case=Depends(add_flashcard_use_case), current_user: str = Depends(get_current_user)):
    add_flashcard_use_case.execute(lemma=lemma, user_id=current_user)
    """Create a new flashcard."""
    return {"message": "Flashcard created."}

@router.post("/{flashcard_id}/add_sentence")
async def add_sentence_to_flashcard(flashcard_id: str, sentence: str, add_sentence_use_case=Depends(add_sentence_use_case), current_user: str = Depends(get_current_user)):
    """Add a sentence to an existing flashcard."""
    add_sentence_use_case.execute(flashcard_id=flashcard_id, user_id=current_user, sentence=sentence)
    return {"message": "Sentence added to flashcard."}