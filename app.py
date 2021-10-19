from flask import Flask, flash, redirect, render_template, request, session

from tempfile import mkdtemp
from io import BytesIO

import requests

from utils import serve_PIL_image
from image_processor import generate_meme

from PIL import Image

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


#@app.route("/")
#def index():
#    """Show index.html"""
#
#    return render_template("index.html")


@app.route("/", methods=["GET"])
def user_inputs():
    """"""

    #if request.method == "POST":

    return render_template("user_inputs.html")


@app.route("/make_meme", methods=["POST"])
def make_meme():
    """
    """
    #assert request.form["img_url"] is not None and request.form["img_url"] != ""

    print("Request-form:", request.form)
    print("Request-form img_url:", request.form["img_url"])
    print("Request-files:", request.files)
    #print(request.form["filename"])
    #print(filename.filename)

    #if request.form["filename"] and request.form["filename"] != "":
    #    f = request.form["filename"].read()
    #    print(f)
    #    #stream = BytesIO(f.read())

    #if request
    img_file = None
    if "img_file" in request.files and request.files['img_file'].filename != "":
        #print("img_file in files")
        img_file = request.files['img_file']
        # TODO: check that is allowed file type
        #img_file = BytesIO(f.read())
        #test_img1 = Image.open(f)
        #print(test_img1.size)
        #test_img2 = Image.open(f.read())
        #print(test_img2.size)
        #test_img3 = Image.open(BytesIO(f.read()))
        #print(test_img3.size)

    img_url = None
    if "img_url" in request.form and request.form["img_url"] != "":
        img_url = request.form["img_url"]

    meme_img = generate_meme(url = img_url, img_path = img_file, 
                             toptext = request.form["upper_text"],
                             color_hex = request.form["upper_text_color"], 
                             transparency = 0.01 * float(request.form["transparency"]))

    #return render_template("generated_meme.html", img=meme_img)
    return serve_PIL_image(meme_img, as_attachment=False)


