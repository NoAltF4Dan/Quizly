import yt_dlp
import os
from core.settings import ydl_opts

def download_audio(url) -> str:
    """Function that downloads audio from a given URL using yt-dlp and returns the absolute path to the saved .m4a file."""
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        output_path = ydl.prepare_filename(info)
        base, ext = os.path.splitext(output_path)
        final_path = base + ".m4a"
        return os.path.abspath(final_path)
    
