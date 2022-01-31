from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from models import FileStore, fs


@dataclass
class FileModel(ABC):
    filename: str
    file_store: FileStore = field(default=fs, init=False)

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass
