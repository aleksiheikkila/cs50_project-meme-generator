from io import BytesIO

from PIL import Image, ImageDraw, ImageFont, ImageColor
from typing import Tuple
import requests


FONT_FP = "./fonts/impact.ttf"

# pixel offset from the bottom where the bottom text will be placed
BOTTOMTEXT_MARGIN = 15

# Base image is scaled down to this max size in pixels, keeping aspect ratio
IMAGE_MAX_SIZE = (640, 640)


def get_img_from_url(url:str) -> "Image|None":
    """Returns a PIL Image"""
    
    print("Trying to get an image from url:", url)
    try:
        resp = requests.get(url)
    except Exception as e:
        print("Couldn't get url:", url)
        print(e)
        return None
    
    if resp.status_code != 200:
        print("Couldn't get url (status_code != 200):", url)
        return None
    
    try:
        img = Image.open(BytesIO(resp.content))
    except Exception as e:
        print("Couldn't load an image from url:", url)
        print(e)
        return None

    return img


def get_base_image(url=None, img_path=None, max_size=IMAGE_MAX_SIZE):
    if not url and not img_path:
        return None

    if url is not None:
        img = get_img_from_url(url)
    else:
        print("Trying to use image file from:", img_path)

        try:
            img = Image.open(img_path)
        except Exception as e:
            print("Could not load file from:", img_path)
            print(e)
            img = None

    if img:
        img.thumbnail(max_size)

    return img


def get_font_and_text_size(img_size: Tuple[int, int], 
                           text: str, 
                           font_fp: str,
                           start_size_factor=0.25) -> Tuple[int, int]:
    """Try to find a font size that will make the given text fit on one line
    img_size: [width, height]
    """

    font_size = int(start_size_factor * img_size[1])
    font = ImageFont.truetype(font_fp, font_size)
    text_size = font.getsize(text)

    while text_size[0] > img_size[0] - 20:
        font_size -= 1
        font = ImageFont.truetype(font_fp, font_size)
        text_size = font.getsize(text)

    return font, text_size
 

def draw_text_emphasis(drawing_context: ImageDraw, 
                       text: str, 
                       font: ImageFont, 
                       text_pos: Tuple[int, int], 
                       inverse_effect_size: int = 15, 
                       max_outline_range: int = 20) -> None:
    """draw outlines
    # there may be a better way
    # this is to draw black kind of border / emphasis around the white text
    """
    outline_rng = int(font.size / inverse_effect_size)
    outline_rng = min(outline_rng, max_outline_range)
    for x in range(-outline_rng, outline_rng + 1):
        for y in range(-outline_rng, outline_rng + 1):
            drawing_context.text((text_pos[0] + x, text_pos[1] + y), text, (0,0,0), font=font)


def generate_meme(url: str, 
                  img_path: str, 
                  toptext: str = None, 
                  bottomtext: str = None, 
                  color_hex: str = "#c7e7e8", 
                  transparency: float = 0.50,
                  save_to: str = None) -> "Image|None":


    img = get_base_image(url, img_path)
    if img is None:
        return None

    if not toptext and not bottomtext:
        # Nothing to do
        return img

    try:
        img = img.convert("RGBA")
        img_sz = img.size

        rgb_color = ImageColor.getcolor(color_hex, "RGB")
        rgba_color = [n for n in rgb_color] + [round(transparency * 255)]
        rgba_color = tuple(rgba_color)

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        # get a drawing context
        draw = ImageDraw.Draw(txt)

        if toptext:
            toptext_font, toptext_size = get_font_and_text_size(img_sz, toptext, FONT_FP)
            # find top centered position for top text
            toptext_x = (img_sz[0] / 2) - (toptext_size[0] / 2)
            toptext_y = 0
            toptext_pos = (toptext_x, toptext_y)
            
            draw_text_emphasis(drawing_context=draw, text=toptext, font=toptext_font, 
                               text_pos=toptext_pos)

            draw.text(toptext_pos, toptext, rgba_color, font=toptext_font)
        
        if bottomtext:
            bottomtext_font, bottomtext_size = get_font_and_text_size(img_sz, bottomtext, FONT_FP)
            # find bottom centered position for bottom text
            bottomtext_x = (img_sz[0] / 2) - (bottomtext_size[0] / 2)
            bottomtext_y = img_sz[1] - bottomtext_size[1] - BOTTOMTEXT_MARGIN
            bottomtext_pos = (bottomtext_x, bottomtext_y) 

            draw_text_emphasis(drawing_context=draw, text=bottomtext, font=bottomtext_font, 
                                text_pos=bottomtext_pos)

            draw.text(bottomtext_pos, bottomtext, rgba_color, font=bottomtext_font)

        # Combine layers
        combined = Image.alpha_composite(img, txt)
    
    except Exception as e:
        print(e)
        return None

    # Write to disk
    if save_to:
        combined.save(save_to)

    return combined
