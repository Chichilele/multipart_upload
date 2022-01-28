import os
from random import shuffle
from typing import List
import requests


def read_chunk(file_object, chunk_size=1024 * 100) -> bytes:
    data = file_object.read(chunk_size)
    while data:
        yield data
        data = file_object.read(chunk_size)


def get_chunks(content_path: str) -> dict:
    chunks = {}
    with open(content_path, "rb") as f:
        for i, chunk in enumerate(read_chunk(f)):
            chunks[i] = chunk
    return chunks


def shuffle_dict_keys(chunks: dict) -> List[int]:
    keys: List[int] = list(chunks.keys())
    shuffle(keys)
    return keys


def main(fname, localpath, url):
    content_path = os.path.abspath(fname)
    print(f"Sending chunks of: {content_path}")
    chunks = get_chunks(content_path)

    keys = shuffle_dict_keys(chunks)

    chunk_size: int = 1024 * 100
    chunked_content_path: str = content_path + ".chunked.png"
    for chunk_id in keys:
        with open(chunked_content_path, "wb") as f:
            chunk = chunks[chunk_id]
            f.seek(chunk_size * chunk_id)
            f.write(chunk)

    print(f"Sending chunks of: {chunked_content_path}")
    return
    for i in keys:
        r = requests.post(url, data=chunks[i], headers={"dxchunkid": str(i)})
        print(f"chunk {i:3}\tr: {r}")


if __name__ == "__main__":
    filename = "image.png"  # ~1GB
    localpath = "uploads"
    url = "http://localhost:8080/upload/{0}".format(filename)
    main(filename, url)
