from models import ChunkedFile
from models.chunk import Chunk


class ChunkedFileUploader:
    """Chunked file uploader."""

    def __init__(self) -> None:
        pass

    def start(self, filename: str, nb_chunks: int, chunk_size: int) -> dict:
        """Start a multi part file upload.

        Args:
            filename (str): name of the file to upload.
            nb_chunks (int): number of chunks to part the file in.
            chunk_size (int): size of each chunk.

        Returns:
            dct: resource info.
        """
        chunked_file = ChunkedFile(filename, nb_chunks, chunk_size)
        chunked_file.create()

        return chunked_file.get()

    def upload_chunk(
        self, filename, chunk_id: int, chunk_size: int, chunk_data: bytes
    ) -> Chunk:
        chunked_file = ChunkedFile.load(filename)

        chunk = chunked_file.add_chunk(chunk_id, chunk_size, chunk_data)

        return chunk


from file_uploader import ChunkedFileUploader

# cfu = ChunkedFileUploader()
# cfu.start("image.png", 24, 1024 * 100)
