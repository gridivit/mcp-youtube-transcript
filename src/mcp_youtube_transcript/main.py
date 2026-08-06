from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript, CouldNotRetrieveTranscript

# https://www.youtube.com/watch?v=Nm3MsnngCJg&pp=ugUEEgJydQ%3D%3D



def get_first_transcript_safely(ytt_api, video_id: str):
    try:
        transcript_list = ytt_api.list(video_id)
        # Безопасно берём первый
        first = next(iter(transcript_list), None)
        if first is None:
            print("Нет доступных транскриптов")
            return None
        print(f"Язык: {first.language} [{first.language_code}], авто: {first.is_generated}")
        return first.fetch()
    except CouldNotRetrieveTranscript as e:
        # Ловит TranscriptsDisabled, NoTranscriptFound, VideoUnavailable,
        # RequestBlocked, AgeRestricted и т.д.
        print(f"Не удалось получить транскрипт: {e}")
        return None


if __name__ == "__main__":
    ytt_api = YouTubeTranscriptApi()
    video_id = "Nm3MsnngCJg"
    fetched = get_first_transcript_safely(ytt_api, video_id)
    plain_text = " ".join(snippet.text for snippet in fetched)

    print()