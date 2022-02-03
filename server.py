from random import shuffle
from typing import List
from flask import Flask, request, abort, jsonify
from werkzeug.utils import secure_filename
import os
from file_uploader import ChunkedFileUploader

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads/"

from models import fs

fs.init_app(app)


def shuffle_dict_keys(chunks: dict) -> List[int]:
    keys: List[int] = list(chunks.keys())
    shuffle(keys)
    return keys


def chunk_to_file(
    chunk: bytes,
    index: int,
    dir: str,
) -> int:
    with open(os.path.join(dir, str(index) + ".chunk"), "wb") as fd:
        bytes_written = fd.write(chunk)
    return bytes_written


def write_chunk(path, fd):
    with open(path, "rb") as chunk_fd:
        chunk = chunk_fd.read()
        return fd.write(chunk)


def build_file_from_chunks(
    filename: str,
    chunks_dir: str,
    chunks_nb: int,
) -> None:
    with open(filename, "wb") as fd:
        for i in range(chunks_nb):
            chunk_path = os.path.join(chunks_dir, f"{i}.chunk")
            write_chunk(chunk_path, fd)


@app.route("/files/", methods=["POST"])
@app.route("/files", methods=["POST"])
def files():
    request_data = request.json
    if not request_data:
        abort(400)

    filename = request_data["filename"]
    nb_chunks = request_data["nb_chunks"]
    chunk_size = request_data["chunk_size"]

    uploader = ChunkedFileUploader()
    upload_info = uploader.start(filename, nb_chunks, chunk_size)

    return jsonify(upload_info), 201


@app.route("/upload/<filename>", methods=["POST"])
def upload_process(filename):
    filename = secure_filename(filename)
    fileFullPath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    print(f"HEADERS: \n{request.headers}")
    chunk_id = int(request.headers["dxchunkid"])
    print(f"chunk_id: {chunk_id}\n")
    chunk = request.stream.read(1024 * 100)

    with open(fileFullPath, "wb") as f:
        chunk_size = 1024 * 100
        f.seek(chunk_size * chunk_id)
        f.write(chunk)
    return jsonify({"filename": filename})

    print(f"chunks to: {chunks_dir}")
    for index in shuffled_keys:
        chunk_to_file(chunks[index], index, chunks_dir)

    build_file_from_chunks("rebuilt.png", chunks_dir, chunks_nb)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=True)
