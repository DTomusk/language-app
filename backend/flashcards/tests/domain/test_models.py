from uuid import uuid4
import pytest

from backend.flashcards.domain.models import Flashcard, Lemma

# region Flashcard Tests
def test_flashcard_initialization():
    id = uuid4()
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(id, user_id, lemma)
    
    assert flashcard.id == id
    assert flashcard.user_id == user_id
    assert flashcard.lemma == lemma
    assert flashcard.sentences == []

def test_add_sentence():
    id = uuid4()
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(id, user_id, lemma)
    
    sentence_text1 = "This is a test sentence."
    sentence_text2 = "This is another test sentence."

    flashcard.add_sentence(sentence_text1)
    flashcard.add_sentence(sentence_text2)
    
    assert len(flashcard.sentences) == 2
    assert flashcard.sentences[0].text == sentence_text1
    assert flashcard.sentences[1].text == sentence_text2

def test_add_duplicate_sentence():
    id = uuid4()
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(id, user_id, lemma)
    
    sentence_text = "This is a test sentence."
    flashcard.add_sentence(sentence_text)
    
    with pytest.raises(ValueError):
        flashcard.add_sentence(sentence_text)
# endregion