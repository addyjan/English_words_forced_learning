from app.models import WordItem
from app.session import PracticeSession


def test_wrong_answer_requeues_word_until_threshold() -> None:
    session = PracticeSession([WordItem("apple", "苹果")], repeat_threshold=3)

    first = session.submit("香蕉")
    second = session.submit("梨")
    third = session.submit("桃子")

    assert first.is_correct is False
    assert second.is_correct is False
    assert third.is_correct is False
    assert third.mistakes == 3


def test_correct_answer_clears_mistake_counter() -> None:
    session = PracticeSession([WordItem("library", "图书馆")], repeat_threshold=3)

    session.submit("公园")
    result = session.submit("图书馆")

    assert result.is_correct is True
    assert session.wrong_counts == {}
