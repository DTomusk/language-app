from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True)
class Lemma:
    text: str

@dataclass(frozen=True)
class Sentence:
    text: str

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

class User:
    def __init__(self):
        self.id = uuid4()
        self.flashcards = []

    def add_flashcard(self, lemma: Lemma):
        flashcard = Flashcard(self.id, lemma)
        self.flashcards.append(flashcard)
        return flashcard

    def get_flashcards(self):
        return self.flashcards