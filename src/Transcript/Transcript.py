import math
import re
from difflib import SequenceMatcher
from typing import Dict, List
from typing_extensions import Self

from more_itertools import grouper


class Transcript:
    segments: List[Dict[str, float | str]]
    frames_per_second: int

    def __init__(self, transcript: list[dict[str, any]]=None, fps=30):
        if transcript is not None:
            self.segments = transcript
        else:
            self.segments = []
        self.frames_per_second = fps

    def load_transcript(self, src_file: str):
        lines = []
        with open(src_file, 'r') as infile:
            for line in infile:
                striped_line = line.strip()
                if striped_line:
                    lines.append(striped_line)
            infile.close()

        for timecodes, speaker, text in grouper(lines, 3):
            match = re.match("(\d{2}:\d{2}:\d{2}:\d{2})\s*-\s*(\d{2}:\d{2}:\d{2}:\d{2})", timecodes)
            start = self._compute_timestamp(match.group(1))
            end = self._compute_timestamp(match.group(2))

            seg = {"start": start, "end": end, "text": text}
            self.segments.append(seg)

    def collapse_timestamps(self, start: float, end: float, i=0) -> int:
        # Get the starting segment
        while len(self.segments) > i and self.segments[i]["start"] < start:
            i += 1

        if len(self.segments) <= i + 1:
            return i

        while len(self.segments) > i + 1 and self.segments[i + 1]["end"] < end:
            self.segments[i]["text"] += " " + self.segments[i + 1]["text"].strip()
            self.segments[i]["end"] = self.segments[i + 1]["end"]
            del self.segments[i + 1]

        self.segments[i]["start"] = start
        self.segments[i]["end"] = end

        return i + 1

    def align_to_other(self, other: Self):
        i = 0
        for seg in other.segments:
            constructed_text = ""
            for my_seg in self.segments:
                if seg["text"] is None or my_seg["text"] is None:
                    continue
                similar = self._find_similar_substring(seg["text"], my_seg["text"])
                if len(similar) > 0:
                    print(similar)

    def _find_similar_substring(self, main_string, substring, threshold=0.6):
        """
        Find a similar substring within a larger string using difflib with a threshold.

        Args:
        main_string (str): The larger string.
        substring (str): The substring to search for.
        threshold (float): The similarity threshold (0.0 to 1.0).

        Returns:
        str: The similar substring if found, or an empty string if not found.
        """
        for i in range(0, len(main_string) - 1):
            checking = main_string[:-i]
            matcher = SequenceMatcher(None, checking, substring)
            if matcher.ratio() > threshold:
                return checking

        return ""

    def output_to_file(self, dest: str):
        file = open(dest, "w")
        for seg in self.segments:
            file.write(self._format_timestamp(seg["start"]) + " - " + self._format_timestamp(seg["end"]) + "\n")
            file.write("Unknown\n")
            file.write(seg["text"].strip() + "\n")
            file.write("\n")

        file.close()

    def _format_timestamp(self, timecode: float) -> str:
        split = math.modf(timecode)
        frames = int(split[0] * self.frames_per_second)
        seconds = int(split[1])
        minutes = int(seconds / 60)
        seconds = seconds % 60
        hours = int(minutes / 60)
        minutes %= 60

        return "{:02d}:{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds, frames)

    def _compute_timestamp(self, timecode: str) -> float:
        match = re.match("(\d{2}):(\d{2}):(\d{2}):(\d{2})", timecode)
        hours = float(match.group(1))
        minutes = float(match.group(2))
        seconds = float(match.group(3))
        frames = float(match.group(4))
        return (hours * 60 + minutes) * 60 + seconds + (frames / self.frames_per_second)
