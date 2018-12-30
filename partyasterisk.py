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
    session,
    url_for,
)
from werkzeug import secure_filename

from imageparty import throw_party


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
app.secret_key = "YnWFsvE5fIERUW7jXdwtFnnFldw"


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
        out_path = "data:image/gif;base64, " + throw_party(img)
        return render_template("party.html", img_src=out_path)
