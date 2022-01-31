from dataclasses import dataclass, field
import os

from models import FileModel


@dataclass
class Chunk(FileModel):
    id: int

    def get_filename(self) -> str:
        return self.filename

    def get_chunk_filename(self) -> str:
        return self.filename

    def save(self, data: bytes, chunks_folder: str):
        chunk_abs_path = os.path.join(
            os.path.abspath(self.file_store.file_store_root),
            chunks_folder,
            self.filename,
        )
        with open(chunk_abs_path, mode="wb") as fd:
            fd.write(data)

    def get_data(self, chunks_folder: str) -> bytes:
        chunk_abs_path = os.path.join(
            os.path.abspath(self.file_store.file_store_root),
            chunks_folder,
            self.filename,
        )
        with open(chunk_abs_path, mode="rb") as fd:
            data = fd.read()

        return data

    def delete(self):
        os.remove(self.filename)
