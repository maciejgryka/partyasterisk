import os
from logging.config import dictConfig

import numpy as np
from PIL import Image
from flask import Flask, render_template, request
from imageparty import throw_party


ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg"])
DEBUG = bool(os.environ.get("DEBUG"))
SECRET_KEY = os.environ.get("SECRET_KEY", 'supersekrit')


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024
app.secret_key = SECRET_KEY


def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


def resize(fp, size: tuple = (128, 128)) -> np.array:
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
