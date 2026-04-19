from __future__ import annotations

import random
from dataclasses import dataclass, field

from app.models import PracticeResult, WordItem


@dataclass
class PracticeSession:
    words: list[WordItem]
    repeat_threshold: int = 3
    queue: list[WordItem] = field(init=False)
    wrong_counts: dict[str, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.words:
            raise ValueError("words cannot be empty")
        self.queue = self.words.copy()
        random.shuffle(self.queue)

    def current(self) -> WordItem:
        return self.queue[0]

    def submit(self, answer: str) -> PracticeResult:
        word = self.queue.pop(0)
        normalized_answer = answer.strip().lower()
        normalized_expected = word.translation.strip().lower()
        correct = normalized_answer == normalized_expected

        if correct:
            self.wrong_counts.pop(word.word, None)
        else:
            self.wrong_counts[word.word] = self.wrong_counts.get(word.word, 0) + 1
            if self.wrong_counts[word.word] < self.repeat_threshold:
                self.queue.append(word)

        if not self.queue:
            self.queue = self.words.copy()
            random.shuffle(self.queue)

        return PracticeResult(
            expected=word.translation,
            answer=answer,
            is_correct=correct,
            mistakes=self.wrong_counts.get(word.word, 0),
        )

    def progress(self) -> dict[str, int]:
        return {
            "total": len(self.words),
            "remaining": len(self.queue),
            "active_mistakes": sum(self.wrong_counts.values()),
        }
