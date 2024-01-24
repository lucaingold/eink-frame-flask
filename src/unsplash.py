import logging
from PIL import Image
from pip._vendor.six import BytesIO
import requests
from enum import Enum
from urllib.parse import quote
from flask import current_app


class Orientation(Enum):
    HORIZONTALLY = "landscape"
    VERTICALLY = "Vertically"


class UnsplashAPI:
    def __init__(self):
        self.api_host = current_app.config['PHOTO_API_HOST']
        self.client_id = current_app.config['PHOTO_CLIENT_ID']
        self.screen_ratio = float(current_app.config['SCREEN_ASPECT_RATIO'])
        self.screen_width = current_app.config['SCREEN_WIDTH']
        self.screen_height = current_app.config['SCREEN_HEIGHT']
        pass

    def search_photo_by_keywords(self, keywords, orientation, is_random=False):
        global img
        try:
            if self.client_id is None:
                raise Exception("Missing client id key.")

            url = self.trigger_request(orientation, keywords, is_random)

            response = requests.get(url)

            img = Image.open(BytesIO(response.content))

            if orientation == Orientation.VERTICALLY.name:
                img = img.rotate(-90, expand=True)

            print(f"Successfully found {orientation} photo with keywords '{keywords}'")

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

    def trigger_request(self, orientation, keywords, is_random):
        if orientation == Orientation.VERTICALLY.name:
            api_orientation = 'portrait'
        else:
            api_orientation = 'landscape'
        if is_random:
            url = f"{self.api_host}/photos/random?client_id={self.client_id}&orientation={api_orientation}&query={quote(str(keywords))}"
        else:
            url = f"{self.api_host}/search/photos?client_id={self.client_id}&orientation={api_orientation}&query={quote(str(keywords))}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text) + 'URL:' + url)
        data = response.json()
        if is_random:
            return data["urls"]["regular"]
        else:
            return data["results"][0]["urls"]["regular"]
