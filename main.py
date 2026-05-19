"""Colour Palette Generator — Day 92.

Upload an image and the app reports the 10 most common colours in it,
inspired by Flat UI Colors and coolphptools' colour extractor.

The colour-counting is done with NumPy (Day 76: image processing).
"""

import base64
import io

import numpy as np
from flask import Flask, render_template, request
from PIL import Image, UnidentifiedImageError

app = Flask(__name__)

# Reject anything bigger than 10 MB before it reaches our code.
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}


def extract_colours(image, top_n=10, bucket=24):
    """Return the ``top_n`` most common colours in ``image``.

    How it works (all NumPy):
      1. Shrink the image so even large uploads process instantly.
      2. Turn every pixel into a row of [R, G, B] values.
      3. Snap each pixel into a colour "bucket" so near-identical shades
         (e.g. 50 slightly different blues) count as one colour.
      4. Count how many pixels landed in each bucket and keep the busiest.
      5. For each winning bucket, average the *real* pixels inside it so the
         swatch we show is true to the photo, not just the bucket corner.
    """
    image = image.convert("RGB")
    image.thumbnail((300, 300))  # keeps aspect ratio; ~90k pixels max

    pixels = np.array(image).reshape(-1, 3)
    total_pixels = pixels.shape[0]

    # Snap colours onto a coarse grid to merge similar shades.
    buckets = (pixels // bucket) * bucket
    unique_buckets, counts = np.unique(buckets, axis=0, return_counts=True)

    # Indexes of the top_n busiest buckets, most common first.
    ranking = np.argsort(counts)[::-1][:top_n]

    palette = []
    for index in ranking:
        in_bucket = np.all(buckets == unique_buckets[index], axis=1)
        r, g, b = (int(c) for c in pixels[in_bucket].mean(axis=0).round())
        palette.append(
            {
                "hex": f"#{r:02X}{g:02X}{b:02X}",
                "rgb": f"rgb({r}, {g}, {b})",
                "percent": round(counts[index] / total_pixels * 100, 1),
            }
        )
    return palette


def is_allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("index.html")

    uploaded = request.files.get("image")
    if uploaded is None or uploaded.filename == "":
        return render_template("index.html", error="Please choose an image first.")

    if not is_allowed(uploaded.filename):
        return render_template(
            "index.html",
            error="Unsupported file type. Use PNG, JPG, GIF, BMP or WEBP.",
        )

    raw = uploaded.read()
    try:
        image = Image.open(io.BytesIO(raw))
        palette = extract_colours(image)
    except (UnidentifiedImageError, OSError):
        return render_template(
            "index.html", error="Couldn't read that image — try another file."
        )

    # Base64-encode the upload so we can show it back without saving to disk.
    preview = base64.b64encode(raw).decode("utf-8")
    preview_uri = f"data:{uploaded.mimetype};base64,{preview}"

    return render_template("index.html", palette=palette, preview=preview_uri)


@app.errorhandler(413)
def file_too_large(_error):
    return (
        render_template("index.html", error="That image is too large (max 10 MB)."),
        413,
    )


if __name__ == "__main__":
    app.run(debug=True)
