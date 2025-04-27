from uuid import uuid4
import pytest

from backend.flashcards.domain.models import User, Flashcard, Lemma, Sentence

# region User Tests
def test_user_initialization():
    user_id = uuid4()
    user = User(user_id)
    assert user.id == user_id
    assert user.flashcards == []

def test_add_flashcard():
    user_id = uuid4()
    user = User(user_id)
    lemma = Lemma(text="example")
    flashcard = user.add_flashcard(lemma)
    
    assert len(user.flashcards) == 1
    assert user.flashcards[0] == flashcard
    assert flashcard.lemma == lemma
    assert flashcard.user_id == user_id

def test_add_duplicate_flashcard():
    user_id = uuid4()
    user = User(user_id)
    lemma = Lemma(text="example")
    user.add_flashcard(lemma)
    
    with pytest.raises(ValueError):
        user.add_flashcard(lemma)

def test_get_flashcards():
    user_id = uuid4()
    user = User(user_id)
    lemma1 = Lemma(text="example1")
    lemma2 = Lemma(text="example2")
    
    flashcard1 = user.add_flashcard(lemma1)
    flashcard2 = user.add_flashcard(lemma2)
    
    flashcards = user.get_flashcards()
    
    assert len(flashcards) == 2
    assert flashcards[0] == flashcard1
    assert flashcards[1] == flashcard2
# endregion

# region Flashcard Tests
def test_flashcard_initialization():
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(user_id, lemma)
    
    assert flashcard.user_id == user_id
    assert flashcard.lemma == lemma
    assert flashcard.sentences == []

def test_add_sentence():
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(user_id, lemma)
    
    sentence_text1 = "This is a test sentence."
    sentence_text2 = "This is another test sentence."

    flashcard.add_sentence(sentence_text1)
    flashcard.add_sentence(sentence_text2)
    
    assert len(flashcard.sentences) == 2
    assert flashcard.sentences[0].text == sentence_text1
    assert flashcard.sentences[1].text == sentence_text2

def test_add_duplicate_sentence():
    user_id = uuid4()
    lemma = Lemma(text="example")
    flashcard = Flashcard(user_id, lemma)
    
    sentence_text = "This is a test sentence."
    flashcard.add_sentence(sentence_text)
    
    with pytest.raises(ValueError):
        flashcard.add_sentence(sentence_text)
# endregion