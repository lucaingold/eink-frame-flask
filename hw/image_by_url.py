import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
import requests
from enum import Enum
from urllib.parse import quote

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200

class Orientation(Enum):
    HORIZONTALLY = "landscape"
    VERTICALLY = "Vertically"


def show_from_url(url, orientation):
    global img
    try:
        if url is None:
            raise Exception("Missing url.")

        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        if orientation == Orientation.VERTICALLY.name:
            img = img.rotate(-90, expand=True)

        print(f"Successfully found {orientation} photo for url '{url}'")

        return crop_and_resize_image(img)

    except BaseException as e:
        logging.error(e)
        return None


def crop_and_resize_image(img):
    try:
        # Crop the image to a 4:3 aspect ratio
        aspect_ratio = 4 / 3
        new_width = int(img.height * aspect_ratio)
        left_margin = (img.width - new_width) // 2
        right_margin = img.width - left_margin
        cropped_img = img.crop((left_margin, 0, right_margin, img.height))

        # Resize the image to 1600x1200
        resized_img = cropped_img.resize((SCREEN_WIDTH, SCREEN_HEIGHT))

        return resized_img
    except Exception as e:
        logging.error(f"Error in crop_and_resize_image: {e}")
        return None