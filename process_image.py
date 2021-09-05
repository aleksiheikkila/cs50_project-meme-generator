from PIL import Image, ImageDraw, ImageFont, ImageColor
from pathlib import Path
from io import BytesIO

import argparse
import requests

from typing import Tuple

parser = argparse.ArgumentParser(description='Meme gen')
parser.add_argument('--img_fp', type=str,
                    help='Image file for the meme gen',
                    default=r"C:\Users\k64063633\Downloads\scuba-unsplash.jpg")
parser.add_argument('--img_url', type=str,
                    help='Url for the meme gen')
parser.add_argument('-u', type=str, default=None,
                    help='Upper text block')
parser.add_argument('-l', type=str, default=None,
                    help='Lower text block')
parser.add_argument('-c', type=str, default=None,
                    help='Hexadecimal color, e.g. #c7e7e8')


def get_img_from_url(url:str):
    """Returns a PIL Image"""
    print("Trying to get an image from url:", url)
    try:
        resp = requests.get(url)
    except Exception as e:
        #print(e)
        raise RuntimeError("Couldn't get url:", url)
    if resp.status_code != 200:
        raise RuntimeError("Couldn't get url:", url)
    
    try:
        img = Image.open(BytesIO(resp.content))
    except Exception as e:
        #print(e)
        raise RuntimeError("Couldn't load an image from url:", url)

    return img


args = parser.parse_args()


FONT_FP = "fonts/Impact.ttf"

# Now url is the primary. If no url given, use the file path (or its default)
if args.img_url:
    img = get_img_from_url(args.img_url)
else:
    print("Trying to use image file from:", args.img_fp)
    img = Image.open(Path(args.img_fp))


img = img.convert("RGBA")
img_sz = img.size

color_hex = "#c7e7e8"
rgb_color = ImageColor.getcolor(color_hex, "RGB")


topString = "Hello!"
bottomString = "How r u??? No, really, how are you? Everything OK?? WHat?"
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


top_font, top_text_size = get_font_and_text_size(img_sz, topString, FONT_FP)
bottom_font, bottom_text_size = get_font_and_text_size(img_sz, bottomString, FONT_FP)

    


# Scale the font size to make it fit
# Same size for both top and bottom
#while topTextSize[0] > imageSize[0]-20 or bottomTextSize[0] > imageSize[0]-20:
#    fontSize = fontSize - 1
#    font = ImageFont.truetype(FONT_FP, fontSize)
#    topTextSize = font.getsize(topString)
#    bottomTextSize = font.getsize(bottomString)

# find top centered position for top text
topTextPositionX = (img_sz[0]/2) - (top_text_size[0]/2)
topTextPositionY = 0
topTextPosition = (topTextPositionX, topTextPositionY)

# find bottom centered position for bottom text
bottomTextPositionX = (img_sz[0]/2) - (bottom_text_size[0]/2)
bottomTextPositionY = img_sz[1] - bottom_text_size[1] #* bottom_linecount  # added linecount
bottomTextPosition = (bottomTextPositionX, bottomTextPositionY)  


# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', img.size, (255,255,255,0))
# get a drawing context
draw = ImageDraw.Draw(txt)

# draw outlines
# there may be a better way
# this is to draw black kind of border / emphasis around the white text
outlineRange = int(top_font.size / 15)
for x in range(-outlineRange, outlineRange+1):
    for y in range(-outlineRange, outlineRange+1):
        # TODO: why does this work?
        draw.text((topTextPosition[0]+x, topTextPosition[1]+y), topString, (0,0,0), font=top_font)

# TODO: DRY!      
outlineRange = int(bottom_font.size / 15)
for x in range(-outlineRange, outlineRange+1):
    for y in range(-outlineRange, outlineRange+1):
        # TODO: why does this work?
        draw.text((bottomTextPosition[0]+x, bottomTextPosition[1]+y), bottomString, (0,0,0), font=bottom_font)
              

# White text

# draw text, half opacity
rgba_color = [n for n in rgb_color] + [128]
rgba_color = tuple(rgba_color)
draw.text(topTextPosition, topString, rgba_color, font=top_font)  # used rgb_color
draw.text(bottomTextPosition, bottomString, rgba_color, font=bottom_font)


# Combine layers
combined = Image.alpha_composite(img, txt)  

# Write to disk
combined.save("output/temp5.png")


# TODO: Transparency to the text
# Multiline text?
# Any easy way to let the user define the area where the text should fit?