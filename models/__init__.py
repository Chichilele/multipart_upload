import os


class FileStore:
    file_store_root: str

    def __init__(self, file_store_root: str = "uploads") -> None:
        self.file_store_root = file_store_root
        self.create()

    def create(self) -> str:
        if not os.path.exists(self.file_store_root):
            os.mkdir(self.file_store_root)

    def delete(self):
        os.rmdir(self.file_store_root)


class FlaskFileStore(FileStore):
    def __init__(self, app=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.file_store_root = app.config["UPLOAD_FOLDER"]
        self.create


fs = FlaskFileStore()

from models.file_model import FileModel
from models.chunk import Chunk
from models.chunked_file import ChunkedFile
