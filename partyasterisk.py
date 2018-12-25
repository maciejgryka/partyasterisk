import os
from uuid import uuid4
from io import StringIO

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug import secure_filename

from imageparty import throw_party


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), ".")
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def resize(fp, size=(128, 128)):
    """Take an image file object and return a version of it resized to `size` as np.array."""
    img = Image.open(fp)
    img.thumbnail(size, Image.ANTIALIAS)
    return np.array(img)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/party", methods=["POST"])
def party_post():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        img = resize(file)
        out_path = str(uuid4()) + ".gif"
        throw_party(img, out_path)
        return redirect(url_for("party", filename=out_path))


@app.route("/party/<filename>")
def party(filename):
    return render_template(
        "party.html", img_src=url_for("uploaded_file", filename=filename)
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
