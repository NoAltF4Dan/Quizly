import whisper

def transcribe_audio(audio_file):
    """Function that transcribes an audio file into text using the Whisper tiny model."""
    model = whisper.load_model("tiny")
    result = model.transcribe(audio_file)
    return result["text"]