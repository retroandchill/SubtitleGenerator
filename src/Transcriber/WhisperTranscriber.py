import whisper

from Vocabulary.VocabularyList import VocabularyList


class WhisperTranscriber:

    def __init__(self, model: str, vocab: VocabularyList):
        self.model = model
        self.vocab = vocab

    def transcribe(self, audio_file: str):
        model = whisper.load_model(self.model)

        # decode the audio
        prompt = "\n".join(self.vocab.gather_vocabulary())
        result = model.transcribe(audio_file, initial_prompt=prompt)

        # print the recognized text
        print(result["text"])
