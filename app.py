from flask import Flask, flash, redirect, render_template, request, session

from tempfile import mkdtemp

import requests

from utils import serve_PIL_image
from image_processor import generate_meme


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    """Show index.html"""

    return render_template("index.html")


@app.route("/user_inputs", methods=["GET"])
def user_inputs():
    """"""

    #if request.method == "POST":

    return render_template("user_inputs.html")


@app.route("/make_meme", methods=["POST"])
def make_meme():
    """
    """
    assert request.form["img_url"] is not None and request.form["img_url"] != ""

    meme_img = generate_meme(url = request.form["img_url"], img_path = None, 
                             toptext = request.form["upper_text"],
                             color_hex = request.form["upper_text_color"], 
                             transparency = 0.01 * float(request.form["transparency"]))

    #return render_template("generated_meme.html", img=meme_img)
    return serve_PIL_image(meme_img)
