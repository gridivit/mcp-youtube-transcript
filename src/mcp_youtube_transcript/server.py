"""MCP-wrapper under youtube.py"""

import logging

from mcp.server import MCPServer
from youtube_transcript_api import CouldNotRetrieveTranscript, NoTranscriptFound, TranscriptsDisabled

from .youtube import extract_video_id, fetch_text, list_languages

logger = logging.getLogger(__name__)

mcp = MCPServer("youtube-transcript")


@mcp.tool()
def list_transcript_languages(url: str) -> str:
    """List the subtitle tracks available for a YouTube video.

    Call this when you do not know which languages a video has, or after
    get_transcript reported that the requested language is unavailable.

    Args:
        url: YouTube video URL (watch, youtu.be, shorts or embed form),
            or the bare 11-character video id.

    Returns:
        One line per track: "<code> - <name> (manual|auto-generated)".
    """
    video_id = extract_video_id(url)
    logger.info("listing languages for %s", video_id)

    languages = list_languages(video_id)
    if not languages:
        raise ValueError(f"Video {video_id} has no subtitle tracks at all.")

    return "\n".join(
        f"{language.code} - {language.name} ({'auto-generated' if language.is_generated else 'manual'})"
        for language in languages
    )


@mcp.tool()
def get_transcript(url: str, language: str) -> str:
    """Get the full transcript text of a YouTube video.

    Returns the whole transcript as plain text without timestamps. Long videos
    produce long text: a two-hour video is roughly 20-30 thousand words.

    If the requested language is unavailable, English is used as a fallback.
    If neither exists, this fails and lists the languages the video does have -
    pick one of them and call again.

    Args:
        url: YouTube video URL (watch, youtu.be, shorts or embed form),
            or the bare 11-character video id.
        language: Language code of the wanted transcript, e.g. "en", "ru", "de".

    Returns:
        The transcript as a single plain-text string.
    """
    video_id = extract_video_id(url)
    logger.info("fetching transcript for %s in %s", video_id, language)

    try:
        return fetch_text(video_id, language)
    except NoTranscriptFound as error:
        available = ", ".join(item.code for item in list_languages(video_id))
        raise ValueError(
            f"No transcript in {language!r} and no English fallback for {video_id}. "
            f"Available languages: {available}. Call this tool again with one of them."
        ) from error
    except TranscriptsDisabled as error:
        raise ValueError(
            f"The author disabled subtitles for video {video_id}. "
            "No transcript can be retrieved for it."
        ) from error
    except CouldNotRetrieveTranscript as error:
        raise ValueError(
            f"Could not retrieve the transcript for {video_id}: {error}"
        ) from error


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
