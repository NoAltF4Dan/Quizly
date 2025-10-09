import os
import json
from .youtube_service import download_audio
from .transcription_service import transcribe_audio
from .ai_service import generate_quiz

def create_quiz_from_video(video_url: str):
    ):
    """
    Build quiz data from a video URL by downloading audio, transcribing it,
    and generating questions from the transcript.

    Behavior
    --------
    - Deletes any stale temp file at `./media/audiofile.m4a`.
    - `download_audio(video_url)`: fetches audio and returns a local filepath.
    - `transcribe_audio(path)`: produces a full-text transcript.
    - `generate_quiz(transcript)`: returns a JSON string describing the quiz.
    - Parses the JSON into a Python dict and returns it.
    - Cleans up the temp audio file before returning.

    Parameters
    ----------
    video_url : str
        Public or authenticated URL pointing to a supported video resource
        (e.g., YouTube). The underlying downloader must understand the URL.

    Returns
    -------
    dict
        Parsed quiz payload produced by the AI layer. Typical shape:
        {
          "title": str,
          "description": str,
          "questions": [
             {"question_title": str, "question_options": [str, ...], "answer": str},
             ...
          ]
        }

    Side Effects
    ------------
    - Creates and deletes `./media/audiofile.m4a` on disk.
    - Network I/O (video/audio download) and CPU/GPU use for transcription/LLM.

    Errors & Exceptions
    -------------------
    - Propagates downloader errors (e.g., `yt_dlp.utils.DownloadError`) from
      `download_audio`.
    - May raise I/O errors (`FileNotFoundError`, `PermissionError`, `OSError`)
      when touching the temp file.
    - `json.JSONDecodeError` if `generate_quiz` returns invalid JSON.
    - Any unexpected exceptions from the transcription/AI backends will bubble up.

    Security
    --------
    - Does not log or return raw transcripts; only the derived quiz dict is returned.
    - Make sure any downloader/transcriber credentials are handled outside this
      function (env vars, secrets manager) and not embedded in logs.
    - If handling private videos, ensure access tokens are not written to disk.

    Reliability
    -----------
    - Consider wrapping the function in a retry policy for transient network
      failures in `download_audio`.
    - For concurrency, use unique temp filenames (e.g., UUID) or isolated
      work dirs to avoid race conditions on `./media/audiofile.m4a`.

    Observability
    -------------
    - For production, add structured logging around each stage (download,
      transcription, generation) including timings and input size — but avoid
      logging sensitive URLs or transcript content.

    Example
    -------
    >>> data = create_quiz_from_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    >>> data["title"]
    'Intro to ...'
    """
    if os.path.exists('./media/audiofile.m4a'):
        os.remove('./media/audiofile.m4a')
    audio_file = download_audio(video_url)
    transcript = transcribe_audio(audio_file)
    quiz = generate_quiz(transcript)
    data = json.loads(quiz)
    os.remove('./media/audiofile.m4a')
    return data
