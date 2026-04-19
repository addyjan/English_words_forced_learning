from __future__ import annotations

import json
from pathlib import Path

from app.models import WordItem


class WordRepository:
    def __init__(self, source_file: Path) -> None:
        self.source_file = source_file

    def list_words(self) -> list[WordItem]:
        payload = json.loads(self.source_file.read_text(encoding="utf-8"))
        words = [WordItem(word=item["word"].strip(), translation=item["translation"].strip()) for item in payload]
        return [item for item in words if item.word and item.translation]
