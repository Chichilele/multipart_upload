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
    chunks: dict

    def __init__(
        self,
        target_file: str,
        nb_chunks: int,
        chunk_size: int,
        chunks_factory=lambda: {},
    ):
        self.chunks_folder = target_file + "_chunks"
        self.target_file = target_file
        self.nb_chunks = nb_chunks
        self.chunk_size = chunk_size
        self.chunks = chunks_factory()

        info_filename = os.path.join(self.chunks_folder, target_file + ".json")

        super().__init__(filename=info_filename)

    def load(self, filename: str):
        abs_path = os.path.join(self.file_store.file_store_root, self.filename)

        with open(abs_path, "r") as fd:
            file_info = json.load(fd)

        self.chunks_folder = file_info["filename"] + "_chunks"
        self.target_file = file_info["filename"]
        self.nb_chunks = file_info["nb_chunks"]
        self.chunk_size = file_info["chunk_size"]
        self.chunks = self.get_available_chunks(file_info["chunks_info"])

    def get_available_chunks(chunks_info: List[dict]) -> dict:
        chunks = {}
        for chunk_id, chunk_filename in chunks_info.items():
            chunk = Chunk(chunk_filename, chunk_id)
            chunks[chunk.id] = chunk

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
        chunks_info = {chunk.id: chunk.filename for chunk in self.chunks.values()}
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

    def add_chunk(self, new_chunk: Chunk, chunk_data: bytes):
        """Add a new chunk and save it.

        Args:
            chunk_id (int): chunk id.
            chunk_data (bytes): chunk data.

        Returns:
            Chunk: Added chunk object.
        """
        if new_chunk.id > self.nb_chunks:
            raise ValueError("Chunk id bigger than the number of chunks")
        if new_chunk.id in [chunk_id for chunk_id in self.chunks.keys()]:
            raise ValueError("Chunk id already processed.")

        new_chunk.save(chunk_data, self.chunks_folder)
        self.chunks[new_chunk.id] = new_chunk
        self.save()
