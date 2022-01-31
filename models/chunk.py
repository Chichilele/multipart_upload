from dataclasses import dataclass, field
import os

from models import FileModel


@dataclass
class Chunk(FileModel):
    id: int

    def get_filename(self) -> str:
        return self.filename

    def get_chunk_info(self) -> dict:
        return {"chunk_filename": self.chunk_filename, "chunk_id": self.id}

    def save(self, data: bytes):
        chunk_abs_path = os.path.join(
            os.path.abspath(self.file_store.file_store_root), self.filename
        )
        with open(chunk_abs_path, mode="wb") as fd:
            fd.write(data)

    def delete(self):
        os.remove(self.filename)
