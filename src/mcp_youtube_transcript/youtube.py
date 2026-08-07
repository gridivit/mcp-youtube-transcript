from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi

_ID_LENGTH = 11
_MIN_PREFIXED_SEGMENTS = 2
_ID_CHARS = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
)

_YOUTUBE_HOSTS = frozenset(
    {"youtube.com", "m.youtube.com", "music.youtube.com"}
)

_PATH_PREFIXES = frozenset(
    {"shorts", "embed", "live", "v"}
)


@dataclass(frozen=True)
class TranscriptLanguage:

    code: str
    name: str
    is_generated: bool
    is_translatable: bool


def _looks_like_id(value: str) -> bool:
    return len(value) == _ID_LENGTH and all(char in _ID_CHARS for char in value)


def extract_video_id(url: str) -> str:

    candidate = url.strip()

    if _looks_like_id(candidate):
        return candidate

    if "://" not in candidate:
        candidate = "https://" + candidate

    parsed = urlparse(candidate)

    host = (parsed.hostname or "").removeprefix("www.")

    segments = [segment for segment in parsed.path.split("/") if segment]

    if host == "youtu.be":
        if segments and _looks_like_id(segments[0]):
            return segments[0]
    elif host in _YOUTUBE_HOSTS:
        from_query = parse_qs(parsed.query).get("v", [""])[0]
        if _looks_like_id(from_query):
            return from_query

        if (
            len(segments) >= _MIN_PREFIXED_SEGMENTS
            and segments[0] in _PATH_PREFIXES
            and _looks_like_id(segments[1])
        ):
            return segments[1]

    raise ValueError(
        f"Could not extract a video ID from {url!r}. Supported formats are "
        "https://www.youtube.com/watch?v=..., https://youtu.be/..., "
        "https://www.youtube.com/shorts/..., or a bare 11-character ID."
    )


def list_languages(video_id: str) -> list[TranscriptLanguage]:

    api = YouTubeTranscriptApi()

    return [
        TranscriptLanguage(
            code=transcript.language_code,
            name=transcript.language,
            is_generated=transcript.is_generated,
            is_translatable=transcript.is_translatable
        )
        for transcript in api.list(video_id)
    ]


def fetch_text(video_id: str, language: str) -> str:
    api = YouTubeTranscriptApi()
    priority = list(dict.fromkeys([language, "en"]))
    fetched = api.fetch(video_id, languages=priority)

    joined = " ".join(snippet.text for snippet in fetched)

    return " ".join(joined.split())
