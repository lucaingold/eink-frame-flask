import logging
from PIL import Image
import requests
from enum import Enum
from flask import current_app
from io import BytesIO


class Orientation(Enum):
    HORIZONTALLY = "landscape"
    VERTICALLY = "Vertically"


class ImageByUrl:
    def __init__(self):
        self.screen_ratio = float(current_app.config['SCREEN_ASPECT_RATIO'])
        self.screen_width = current_app.config['SCREEN_WIDTH']
        self.screen_height = current_app.config['SCREEN_HEIGHT']
        pass

    def show_from_url(self, url, orientation):
        try:
            if url is None:
                raise Exception("Missing url.")
            response = requests.get(url)
            response.raise_for_status()
            if 'image' not in response.headers['content-type']:
                raise Exception("Invalid content type. Expected an image.")
            img = Image.open(BytesIO(response.content)).convert('RGB')
            if img is None:
                raise Exception("Failed to open the image.")
            if orientation == Orientation.VERTICALLY.name:
                img = img.rotate(-90, expand=True)
            print(f"Successfully found {orientation} photo for url '{url}'")
            return self.crop_and_resize_image(img)
        except BaseException as e:
            logging.error(e)
            return None

    def crop_and_resize_image(self, img):
        try:
            aspect_ratio = 4 / 3
            new_width = int(img.height * aspect_ratio)
            left_margin = (img.width - new_width) // 2
            right_margin = img.width - left_margin
            cropped_img = img.crop((left_margin, 0, right_margin, img.height))
            resized_img = cropped_img.resize((self.screen_width, self.screen_height))
            return resized_img
        except Exception as e:
            logging.error(f"Error in crop_and_resize_image: {e}")
            return None
