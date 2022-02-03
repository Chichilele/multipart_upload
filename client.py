import os
from random import shuffle
from shutil import ExecError
from typing import List
import requests


def read_chunk(fd, chunk_size=1024 * 100) -> bytes:
    data = fd.read(chunk_size)
    while data:
        yield data
        data = fd.read(chunk_size)


def get_chunks(fname: str, chunk_size: int) -> dict:
    chunks = {}
    with open(fname, "rb") as f:
        for i, chunk in enumerate(read_chunk(f, chunk_size)):
            chunks[i] = chunk
    return chunks


def shuffle_dict_keys(chunks: dict) -> List[int]:
    keys: List[int] = list(chunks.keys())
    shuffle(keys)
    return keys


def chunk_upload(fname, dest_dir, url):
    print(f"Sending chunks of: {fname}")
    from file_uploader import ChunkedFileUploader

    # prepare file chunks
    fname = "image.png"
    chunk_size = 1024 * 100
    chunks = get_chunks(fname, chunk_size)
    nb_chunks = len(chunks)

    ## 1. Initiate file upload
    uploader = ChunkedFileUploader()
    uploader.start(filename=fname, nb_chunks=nb_chunks, chunk_size=chunk_size)

    ## 2. Upload chunks in random order
    shuffled_keys = shuffle_dict_keys(chunks)
    for i in shuffled_keys:
        uploader.upload_chunk(fname, i, 1024 * 100, chunks[i])

    ## 3. Finalise the upload
    uploader.finalise(fname)


if __name__ == "__main__":
    fname = "image.png"  # ~1GB
    dest_dir = "uploads"
    url = "http://localhost:8080/upload/{0}".format(fname)
    chunk_upload(fname, dest_dir, url)
