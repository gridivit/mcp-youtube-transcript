import pytest

from mcp_youtube_transcript.youtube import extract_video_id

VIDEO_ID = "dQw4w9WgXcQ"


@pytest.mark.parametrize(
    "url",
    [
        VIDEO_ID,
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=42s&pp=ygUH",
        "https://youtu.be/dQw4w9WgXcQ",
        "https://youtu.be/dQw4w9WgXcQ?si=Ab1Cd2Ef3Gh4",
        "https://www.youtube.com/shorts/dQw4w9WgXcQ",
        "https://www.youtube.com/embed/dQw4w9WgXcQ",
        "https://www.youtube.com/live/dQw4w9WgXcQ",
        "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://music.youtube.com/watch?v=dQw4w9WgXcQ",
        "youtube.com/watch?v=dQw4w9WgXcQ",
        "  https://youtu.be/dQw4w9WgXcQ  ",
    ],
)
def test_extracts_id_from_supported_forms(url: str) -> None:
    assert extract_video_id(url) == VIDEO_ID


def test_accepts_ids_with_dash_and_underscore() -> None:
    assert extract_video_id("https://youtu.be/a-b_C1d2E3f") == "a-b_C1d2E3f"


@pytest.mark.parametrize(
    "url",
    [
        "",
        "   ",
        "https://example.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/feed/subscriptions",
        "https://www.youtube.com/watch?v=short",
        "https://www.youtube.com/watch?list=PL123",
        "https://youtu.be/",
        "just some text",
    ],
)
def test_rejects_unsupported_input(url: str) -> None:
    with pytest.raises(ValueError):
        extract_video_id(url)


def test_error_message_helps_the_agent() -> None:
    bad_url = "https://example.com/watch?v=dQw4w9WgXcQ"

    with pytest.raises(ValueError) as excinfo:
        extract_video_id(bad_url)

    message = str(excinfo.value)

    assert bad_url in message
    assert "youtu.be" in message
