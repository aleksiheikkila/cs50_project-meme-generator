from flask import Flask, render_template, request 
from utils import serve_PIL_image
from image_processor import generate_meme


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/", methods=["GET"])
def index():
    """Render main page"""
    return render_template("index.html")

@app.route("/make_meme", methods=["POST"])
def make_meme():
    """
    Endpoint to write the given text on top of the given image.
    Used in ajax manner.
    """

    img_file = None
    if "img_file" in request.files and request.files['img_file'].filename != "":
        img_file = request.files['img_file']

    img_url = None
    if "img_url" in request.form and request.form["img_url"] != "":
        img_url = request.form["img_url"]
    
    # Generate the meme
    meme_img = generate_meme(url=img_url, 
                             img_path=img_file, 
                             toptext=request.form["upper_text"],
                             bottomtext=request.form["lower_text"],
                             color_hex=request.form["upper_text_color"], 
                             transparency=0.01 * (100. - float(request.form["transparency"])))
    # meme_img is either a PIL.Image or None

    # Serve the image
    return serve_PIL_image(meme_img)
