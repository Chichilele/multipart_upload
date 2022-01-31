from dataclasses import dataclass, field
import os
from typing import List
import json

from models import Chunk, FileModel


@dataclass
class ChunkedFile(FileModel):
    chunks_folder: str
    target_file: str
    nb_chunks: int
    chunk_size: int
    chunks: List[Chunk]

    def __init__(
        self,
        target_file: str,
        nb_chunks: int,
        chunk_size: int,
        chunks_factory=lambda: [],
    ):
        self.chunks_folder = target_file + "_chunks"
        self.target_file = target_file
        self.nb_chunks = nb_chunks
        self.chunk_size = chunk_size
        self.chunks = chunks_factory()

        info_filename = os.path.join(self.chunks_folder, target_file + ".json")

        super().__init__(filename=info_filename)

    @staticmethod
    def load(filename: str) -> "ChunkedFile":
        chunked_file = ChunkedFile(filename, None, None)

        with open(chunked_file.filename, "r") as fd:
            file_info = fd.read()

        chunked_file.chunks_folder = file_info["target_file"] + "_chunks"
        chunked_file.target_file = file_info["target_file"]
        chunked_file.nb_chunks = file_info["nb_chunks"]
        chunked_file.chunk_size = file_info["chunk_size"]
        chunked_file.chunks = ChunkedFile._get_all_chunks(file_info["chunks_info"])

        return chunked_file

    @staticmethod
    def _get_all_chunks(chunks_info: List[dict]) -> List[Chunk]:
        chunks = []
        for chunk_info in chunks_info:
            chunk = Chunk(chunk_info["chunk_filename"], chunk_info["chunk_id"])
            chunks.append(chunk)

        return chunks

    def get(self) -> dict:
        abs_path = os.path.join(self.file_store.file_store_root, self.filename)

        with open(abs_path, "r") as fd:
            file_info = fd.read()

        return file_info

    def create(self):
        abs_path = os.path.join(self.file_store.file_store_root, self.chunks_folder)
        os.mkdir(abs_path)
        self.save()

    def save(self):
        file_info = self.get_chunked_file_info()
        abs_path = os.path.join(self.file_store.file_store_root, self.filename)

        with open(abs_path, "w") as fd:
            json.dump(file_info, fd, indent=4)

    def delete(self):
        abs_path = os.path.join(self.file_store.file_store_root, self.filename)
        os.rmdir(abs_path)

    def get_chunked_file_info(self) -> dict:
        chunks_info = [chunk.get_chunk_info() for chunk in self.chunks]
        chunked_file_info = {
            "filename": self.target_file,
            "nb_chunks": self.nb_chunks,
            "chunk_size": self.chunk_size,
            "completed_chunks": self.get_nb_completed_chunks(),
            "chunks_info": chunks_info,
        }
        return chunked_file_info

    def get_nb_completed_chunks(self) -> int:
        return len(self.chunks)

    def add_chunk(self, chunk_id: int, chunk_size: int, chunk_data: bytes) -> Chunk:
        """Add a new chunk and save it.

        Args:
            chunk_id (int): chunk id.
            chunk_data (bytes): chunk data.

        Returns:
            Chunk: Added chunk object.
        """
        if len(chunk_data) != chunk_size or chunk_size != self.chunk_size:
            raise ValueError("Chunk size doesn't match.")
        if chunk_id > self.nb_chunks:
            raise ValueError("Chunk id bigger than the number of chunks")
        if chunk_id in [chunk.id for chunk in self.chunks]:
            raise ValueError("Chunk id bigger than the number of chunks")

        new_chunk_filename: str = f"{self.target_file}_{id:4}.chunk"
        new_chunk: Chunk = Chunk(new_chunk_filename, chunk_id)
        new_chunk.save(chunk_data)
        self.chunks.append(new_chunk)
        self.save()

        return new_chunk
