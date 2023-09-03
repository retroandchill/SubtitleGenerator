import abc
from typing import List


class VocabularyList(abc.ABC):
    @abc.abstractmethod
    def gather_vocabulary(self, source: str) -> List[str]:
        pass