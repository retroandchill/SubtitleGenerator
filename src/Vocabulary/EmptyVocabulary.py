from typing import List

from Vocabulary.VocabularyList import VocabularyList


class EmptyVocabulary(VocabularyList):

    def gather_vocabulary(self) -> List[str]:
        return []