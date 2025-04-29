from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Lemma:
    text: str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other
        if isinstance(other, Lemma):
            return self.text == other.text
        return False

@dataclass(frozen=True)
class Sentence:
    text: str

    def __eq__(self, other):
        if isinstance(other, str):
            return self.text == other
        if isinstance(other, Sentence):
            return self.text == other.text
        return False

# TODO: flashcards will need to store more metadata for spaced repetition etc.
class Flashcard:
    def __init__(self, user_id: UUID, lemma: Lemma):
        self.id = uuid4()
        self.user_id = user_id
        self.lemma = lemma
        self.sentences = []
    
    def add_sentence(self, text: str):
        if any(sentence == text for sentence in self.sentences):
            raise ValueError("Sentence already exists")
        sentence = Sentence(text)
        self.sentences.append(sentence)

    def __eq__(self, other):
        if isinstance(other, Flashcard):
            return self.user_id == other.user_id and self.lemma == other.lemma
        return False        

class User:
    def __init__(self, user_id: UUID):
        self.id = user_id
        self.flashcards = []

    def add_flashcard(self, lemma: Lemma):
        if any(flashcard.lemma == lemma for flashcard in self.flashcards):
            raise ValueError("Flashcard already exists")
        flashcard = Flashcard(self.id, lemma)
        self.flashcards.append(flashcard)
        return flashcard

    def get_flashcards(self):
        return self.flashcards