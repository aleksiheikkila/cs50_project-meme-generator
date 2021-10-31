#from PIL import Image, ImageDraw, ImageFont, ImageColor
from io import BytesIO
from base64 import b64encode
from urllib.parse import quote


def encode_to_base64(img_io) -> str:
    """"
    Encodes img_io to base64 and adds the necessary 'header'
    """
    data = b64encode(img_io.getvalue()).decode('ascii')
    data_url = 'data:image/png;base64,{}'.format(quote(data))
    return data_url


def serve_PIL_image(pil_img: "Image"|None) -> str:
    """
    Creates BytesIO from PIL Image and encodes that to base64, 
    which is to be sent to the browser and put in the image src.

    In case PIL Image is None, returns path to the file used to notify about errors
    """
    if pil_img is None:
        return "static/error.jpg"

    img_io = BytesIO()
    pil_img.save(img_io, 'PNG')
    img_io.seek(0)

    return encode_to_base64(img_io)
