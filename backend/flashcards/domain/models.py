from dataclasses import dataclass, field
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

# Sentences are value objects accessible only via the aggregate root (Flashcard).
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
# Flashcard is an aggregate root
class Flashcard:
    def __init__(self, id: UUID, user_id: UUID, lemma: Lemma, sentences: list[Sentence] = None):
        self.id = id
        self.user_id = user_id
        self.lemma = lemma
        self.sentences: list[Sentence] = sentences if sentences is not None else []
        # This is so the repo knows which sentences to add
        # while the domain model shouldn't have to worry about the repo 
        # it doesn't make sense to have to figure out what to update each time
        self._added_sentences: list[Sentence] = []
    
    def add_sentence(self, text: str):
        if any(sentence == text for sentence in self.sentences):
            raise ValueError("Sentence already exists")
        sentence = Sentence(text)
        self.sentences.append(sentence)
        self._added_sentences.append(sentence)

    def __eq__(self, other):
        if isinstance(other, Flashcard):
            return self.user_id == other.user_id and self.lemma == other.lemma
        return False        