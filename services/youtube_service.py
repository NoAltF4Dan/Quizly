import yt_dlp
import os
from core.settings import ydl_opts

def download_audio(url) -> str:
    :
    """
    Download audio from a video URL using `yt-dlp` and return the absolute
    path to the resulting `.m4a` file.

    Behavior
    --------
    - Initializes `yt_dlp.YoutubeDL` with `ydl_opts` from settings.
    - `extract_info(url, download=True)` fetches metadata and downloads media.
    - Uses `prepare_filename(info)` to compute the output filename and
      normalizes the extension to `.m4a` for the returned path.
    - Returns an absolute path suitable for downstream consumers.

    Parameters
    ----------
    url : str
        A supported media URL (e.g., YouTube). Must be accessible by `yt-dlp`.

    Returns
    -------
    str
        Absolute filesystem path to the downloaded `.m4a` file.

    Requirements
    ------------
    - `core.settings.ydl_opts` should configure audio extraction, e.g.:
      - `format`: audio-only or bestaudio
      - `outtmpl`: output template (e.g., `./media/%(title)s.%(ext)s`)
      - `postprocessors`: to produce M4A/ALAC if needed
    - Ensure the target directory in `outtmpl` exists and is writable.

    Side Effects
    ------------
    - Writes the audio file (and temp artifacts) to disk according to `outtmpl`.
    - Network I/O and external process invocations via `yt-dlp`.

    Errors & Exceptions
    -------------------
    - Raises `yt_dlp.utils.DownloadError` for invalid/blocked URLs or failures.
    - May raise `OSError`/`PermissionError` if the output path is not writable.
    - The returned extension assumes `.m4a`; if your `ydl_opts` produce a
      different codec/container, adjust the extension logic accordingly.

    Security
    --------
    - Do not log full URLs or credentials if private videos are accessed.
    - Keep `ydl_opts` free of secrets in code; prefer env vars or a secrets store.

    Notes
    -----
    - If multiple files can be produced (e.g., playlists), ensure `ydl_opts`
      restricts to a single entry or adapt this function to handle lists.
    """
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        output_path = ydl.prepare_filename(info)
        base, ext = os.path.splitext(output_path)
        final_path = base + ".m4a"
        return os.path.abspath(final_path)
    
