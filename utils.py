#from PIL import Image, ImageDraw, ImageFont, ImageColor
from io import BytesIO
from flask import send_file

from base64 import b64encode
from urllib.parse import quote


def encode_to_base64(img_io):
    data = b64encode(img_io.getvalue()).decode('ascii')
    data_url = 'data:image/png;base64,{}'.format(quote(data))
    return data_url

def serve_PIL_image(pil_img, quality=70, as_attachment=True, attachment_filename="your_image.png", as_b64=True):
    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)

    if as_b64:
        return encode_to_base64(img_io)

    
    if as_attachment:
        return send_file(img_io, 
                         mimetype='image/png', 
                         as_attachment=as_attachment, 
                         attachment_filename=attachment_filename)
    else:
        return send_file(img_io, mimetype='image/png')
