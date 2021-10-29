from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
from io import BytesIO

import requests

from typing import Tuple

FONT_FP = "./fonts/impact.ttf"
BOTTOMTEXT_MARGIN = 15  # pixel offset from the bottom where the bottom text will be placed


def get_img_from_url(url:str) -> "Image|None":
    """Returns a PIL Image"""
    print("Trying to get an image from url:", url)
    try:
        resp = requests.get(url)
    except Exception as e:
        #print(e)
        #raise RuntimeError("Couldn't get url:", url)
        print("Couldn't get url (Exc in requests):", url)
        return None
    
    if resp.status_code != 200:
        #raise RuntimeError("Couldn't get url:", url)
        print("Couldn't get url (status_code != 200):", url)
        return None
    
    try:
        img = Image.open(BytesIO(resp.content))
    except Exception as e:
        #print(e)
        #raise RuntimeError("Couldn't load an image from url:", url)
        print("Couldn't load an image from url (Exc in Image.open):", url)
        return None

    return img


def get_base_image(url = None, img_path = None, max_size=(640, 640)):
    if not url and not img_path:
        return None

    if url is not None:
        img = get_img_from_url(url)
    else:
        print("Trying to use image file from:", img_path)
        #if use_stream:
        #    with open(img_path, "rb") as f:
        #        stream = BytesIO(f.read())
        #        img = Image.open(stream)
            
        #else:
        try:
            img = Image.open(img_path)
        except:
            img = None

    if img:
        img.thumbnail(max_size)

    return img


def get_font_and_text_size(img_size: Tuple[int, int], text: str, font_fp,
                 start_size_factor=0.25) -> Tuple[int, int]:
    """Try to find a font size that will make the given text fit on one line
    img_size: [width, height]
    """

    # initial size to 1/4 of the height

    font_size = int(start_size_factor * img_size[1])
    font = ImageFont.truetype(font_fp, font_size)
    text_size = font.getsize(text)

    while text_size[0] > img_size[0] - 20:
        font_size -= 1
        font = ImageFont.truetype(font_fp, font_size)
        text_size = font.getsize(text)

    return font, text_size
 

def draw_text_emphasis(drawing_context, text, font, text_pos, 
                        inverse_effect_size=15, max_outline_range=20) -> None:
    # draw outlines
    # there may be a better way
    # this is to draw black kind of border / emphasis around the white text
    # TODO: should the effect size be related to the font size... so like percentage
    outline_rng = int(font.size / inverse_effect_size)
    outline_rng = min(outline_rng, max_outline_range)
    print("outline range:", outline_rng)
    for x in range(-outline_rng, outline_rng + 1):
        for y in range(-outline_rng, outline_rng + 1):
            # TODO: why does this work?
            drawing_context.text((text_pos[0] + x, text_pos[1] + y), text, (0,0,0), font=font)


def generate_meme(url, img_path, 
                  toptext = None, bottomtext = None, 
                  color_hex = "#c7e7e8", transparency = 0.50,
                  save_to = None) -> "Image|None":
    
    #print("transp:", transparency)  # between 0 and 1

    img = get_base_image(url, img_path)
    if img is None:
        #raise RuntimeError("Img is None")
        return None

    if not toptext and not bottomtext:
        # Nothing to do
        return img

    try:
        img = img.convert("RGBA")
        img_sz = img.size
        print("Image size:", img_sz)

        rgb_color = ImageColor.getcolor(color_hex, "RGB")
        rgba_color = [n for n in rgb_color] + [round(transparency * 255)]
        rgba_color = tuple(rgba_color)

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new('RGBA', img.size, (255,255,255,0))
        # get a drawing context
        draw = ImageDraw.Draw(txt)

        # draw text, half opacity
        #rgba_color = [n for n in rgb_color] + [128]
        #rgba_color = tuple(rgba_color)

        if toptext:
            print("Setting top text")
            toptext_font, toptext_size = get_font_and_text_size(img_sz, toptext, FONT_FP)
            
            # find top centered position for top text
            toptext_x = (img_sz[0] / 2) - (toptext_size[0] / 2)
            toptext_y = 0
            toptext_pos = (toptext_x, toptext_y)
            
            #print("Drawing emphasis")
            draw_text_emphasis(drawing_context=draw, text=toptext, font=toptext_font, 
                               text_pos=toptext_pos)

            #print("Drawing text")
            draw.text(toptext_pos, toptext, rgba_color, font=toptext_font)
        
        if bottomtext:
            print("Setting bottom text")
            bottomtext_font, bottomtext_size = get_font_and_text_size(img_sz, bottomtext, FONT_FP)
            # find bottom centered position for bottom text
            bottomtext_x = (img_sz[0] / 2) - (bottomtext_size[0] / 2)
            bottomtext_y = img_sz[1] - bottomtext_size[1] - BOTTOMTEXT_MARGIN
            bottomtext_pos = (bottomtext_x, bottomtext_y) 
            draw_text_emphasis(drawing_context=draw, text=bottomtext, font=bottomtext_font, 
                                text_pos=bottomtext_pos)

            draw.text(bottomtext_pos, bottomtext, rgba_color, font=bottomtext_font)

        # Combine layers
        print("Combining")
        combined = Image.alpha_composite(img, txt)
    
    except Exception as e:
        return None

    # Write to disk
    if save_to:
        combined.save(save_to)

    return combined



#topString = "Hello!"
#bottomString = "How r u??? No, really, how are you? Everything OK?? WHat?"
#bottom_linecount = len(bottomString.split("\n"))
#bottom_maxwidth = max(len(line) for line in bottomString.split("\n"))

# TODO: If there are newlines, should have space for multiple rows

# Now based on:
# https://github.com/danieldiekmeier/memegenerator/blob/master/memegenerator.py

# find biggest font size that works
#fontSize = int(imageSize[1] / 5)  # start with this


# font = ImageFont.truetype("/Library/Fonts/Impact.ttf", fontSize)
#font = ImageFont.truetype(FONT_FP, fontSize)

#font = ImageFont.load_default()

# TODO: How to handle the font thing on some generic machine?
# TODO: Sometimes split to more rows


#topTextSize = font.getsize(topString)
#bottomTextSize = font.getsize(bottomString)



# Scale the font size to make it fit
# Same size for both top and bottom
#while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
#    fontSize = fontSize - 1
#    font = ImageFont.truetype(FONT_FP, fontSize)
#    topTextSize = font.getsize(topString)
#    bottomTextSize = font.getsize(bottomString)




# TODO: Transparency to the text
# Multiline text?
# Any easy way to let the user define the area where the text should fit?
