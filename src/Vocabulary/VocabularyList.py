import abc
from typing import List


class VocabularyList(abc.ABC):
    @abc.abstractmethod
    def gather_vocabulary(self) -> List[str]:
        pass
