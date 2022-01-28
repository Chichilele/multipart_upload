from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "uploads/"


@app.route("/upload/<filename>", methods=["POST", "PUT"])
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("8080"), debug=True)
