# Multipart upload

Flask-multipartupload is a flask extension to facilitate multipart upload.

## Protocole

A plain english explanation can be found [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html).

1. Initiate a new upload and pass file metadata. The interface should return an upload ID to be used for parts upload.
2. Upload each part along with a part number and the upload ID. Reusing a part number replaces any existing part.
3. Complete the upload once all the parts have been uploaded. The target file is then concatenated and all parts are deleted.

```python
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
```
