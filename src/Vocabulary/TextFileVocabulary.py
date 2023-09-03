from typing import List

from Vocabulary.VocabularyList import VocabularyList


class TextFileVocabulary(VocabularyList):

    def __init__(self, source_file):
        self.source_file = source_file

    def gather_vocabulary(self) -> List[str]:
        ret = []
        f = open(self.source_file, "r")
        for line in f:
            ret.append(line.strip())
        return ret
