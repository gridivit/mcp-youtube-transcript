"""Тесты extract_video_id — единственной функции проекта без сети.

Чистый вход, чистый выход: тесты выполняются мгновенно и не зависят
ни от YouTube, ни от моков.
"""

import pytest

from mcp_youtube_transcript.youtube import extract_video_id

VIDEO_ID = "dQw4w9WgXcQ"


@pytest.mark.parametrize(
    "url",
    [
        VIDEO_ID,                                                     # голый ID
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",                # каноническая ссылка
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&pp=ygUH",  # лишние параметры
        "https://youtu.be/dQw4w9WgXcQ",                               # короткая форма
        "https://youtu.be/dQw4w9WgXcQ?si=Ab1Cd2Ef3Gh4",               # с трекингом от "Поделиться"
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/live/dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",                  # мобильный хост
        "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
        "youtube.com/watch?v=dQw4w9WgXcQ",                            # без схемы: агент так тоже пришлёт
        "  https://youtu.be/dQw4w9WgXcQ  ",                           # пробелы по краям после копипасты
    ],
)
def test_extracts_id_from_supported_forms(url: str) -> None:
    assert extract_video_id(url) == VIDEO_ID


def test_accepts_ids_with_dash_and_underscore() -> None:
    # "-" и "_" входят в алфавит ID, но легко теряются при написании регулярок.
    assert extract_video_id("https://youtu.be/a-b_C1d2E3f") == "a-b_C1d2E3f"


@pytest.mark.parametrize(
    "url",
    [
        "",                                            # пустая строка
        "   ",                                         # только пробелы
        "https://example.com/watch?v=dQw4w9WgXcQ",     # похоже на YouTube, но чужой хост
        "https://www.youtube.com/feed/subscriptions",  # YouTube, но не видео
        "https://www.youtube.com/watch?v=short",       # ID короче 11 символов
        "https://www.youtube.com/watch?list=PL123",    # нет параметра v
        "https://youtu.be/",                           # нет сегмента с ID
        "just some text",                              # вообще не ссылка
    ],
)
def test_rejects_unsupported_input(url: str) -> None:
    # pytest.raises падает, если исключения НЕ было — то есть проверяет,
    # что функция не выдумала ID там, где его нет.
    with pytest.raises(ValueError):
        extract_video_id(url)


def test_error_message_helps_the_agent() -> None:
    """Текст ValueError читает модель, поэтому он тоже часть контракта."""
    bad_url = "https://example.com/watch?v=dQw4w9WgXcQ"

    with pytest.raises(ValueError) as excinfo:
        extract_video_id(bad_url)

    message = str(excinfo.value)  # excinfo.value — само исключение, str() даёт его текст

    assert bad_url in message      # агент видит, что именно он прислал
    assert "youtu.be" in message   # и какие формы поддерживаются