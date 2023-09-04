import whisper


class WhisperTranscriber:

    def __init__(self, model: str):
        self.model = model

    def transcribe(self, audio_file: str) -> str:
        model = whisper.load_model(self.model)

        # decode the audio
        result = model.transcribe(audio_file)

        # print the recognized text
        return result["text"]
