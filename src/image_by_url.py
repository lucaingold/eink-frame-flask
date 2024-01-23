import logging
from PIL import Image
from pip._vendor.six import BytesIO
import requests
from enum import Enum
from flask import current_app


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
        aspect_ratio = float(current_app.config['SCREEN_ASPECT_RATIO'])
        new_width = int(img.height * aspect_ratio)
        left_margin = (img.width - new_width) // 2
        right_margin = img.width - left_margin
        cropped_img = img.crop((left_margin, 0, right_margin, img.height))

        resized_img = cropped_img.resize(int(current_app.config['SCREEN_WIDTH']), int(current_app.config['SCREEN_HEIGHT']))

        return resized_img
    except Exception as e:
        logging.error(f"Error in crop_and_resize_image: {e}")
        return None
