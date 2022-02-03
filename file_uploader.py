import os
from models import ChunkedFile
from models.chunk import Chunk


class ChunkedFileUploader:
    """Chunked file uploader."""

    def __init__(self) -> None:
        pass

    def start(self, filename: str, nb_chunks: int, chunk_size: int) -> dict:
        """Start a multi part file upload.

        Args:
            `filename` (str): name of the file to upload.
            `nb_chunks` (int): number of chunks to part the file in.
            `chunk_size` (int): size of each chunk.

        Returns:
            dict: resource info.
        """
        chunked_file = ChunkedFile(filename, nb_chunks, chunk_size)
        chunked_file.create()

        return chunked_file.get()

    def upload_chunk(
        self,
        filename: str,
        chunk_id: int,
        chunk_size: int,
        chunk_data: bytes,
    ) -> Chunk:

        chunked_file = ChunkedFile(filename, None, None)
        chunked_file.load(filename=filename)

        new_chunk_filename: str = f"{filename}_{chunk_id:04}.chunk"
        new_chunk: Chunk = Chunk(new_chunk_filename, chunk_id)

        chunk = chunked_file.add_chunk(new_chunk, chunk_data)

        return chunk

    ## TODO: WIP
    def finalise(self, filename: str):
        chunked_file = ChunkedFile(filename, None, None)
        chunked_file.load(filename=filename)

        with open(filename, "wb") as target_fd:
            for chunk_id, chunk in chunked_file.get_chunks().items():
                chunk_path = os.path.join(chunked_file.chunks_folder, chunk.filename)
                with open(chunk_path, "rb") as f:
                    f.seek(chunked_file.chunk_size * int(chunk_id))
                    f.write(chunk.get_data(chunked_file.chunks_folder))
