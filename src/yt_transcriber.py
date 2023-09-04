import subprocess
import sys
from tempfile import TemporaryDirectory

import ffmpeg

from Transcript.Transcript import Transcript
from Transcriber.WhisperTranscriber import WhisperTranscriber

if __name__ == "__main__":
    transcript = Transcript()
    transcript.load_transcript(sys.argv[2])

    temp_dir = TemporaryDirectory()
    transcriber = WhisperTranscriber("small.en")
    i = 0
    for seg in transcript.segments:
        temp_file = "{0}/temp{1}.wav".format(temp_dir.name, i)
        subprocess.run(["ffmpeg", "-ss", str(seg["start"]), "-t", str(seg["end"] - seg["start"]), "-i", sys.argv[1],
                        temp_file])
        whisper_result = transcriber.transcribe(temp_file)
        seg["text"] = whisper_result
        i += 1

    transcript.output_to_file(sys.argv[3])
