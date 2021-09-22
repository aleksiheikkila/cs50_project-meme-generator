#from PIL import Image, ImageDraw, ImageFont, ImageColor
from io import BytesIO
from flask import send_file


def serve_PIL_image(pil_img, quality=70):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')
