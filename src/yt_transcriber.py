import sys

from Transcriber.WhisperTranscriber import WhisperTranscriber
from Vocabulary.TextFileVocabulary import TextFileVocabulary

vocab = TextFileVocabulary(sys.argv[2])
transcriber = WhisperTranscriber("base", vocab)
transcriber.transcribe(sys.argv[1])
