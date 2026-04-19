from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WordItem:
    word: str
    translation: str


@dataclass
class PracticeResult:
    expected: str
    answer: str
    is_correct: bool
    mistakes: int
