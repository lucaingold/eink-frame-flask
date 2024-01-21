import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
import requests
from enum import Enum
from urllib.parse import quote

API_HOST = 'https://api.unsplash.com'
CLIENT_ID = 'W8cCQ6oXNXAktk17ibvXJlszQ2jvYDZiRc9OXfJ7p6g'
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200


class Orientation(Enum):
    HORIZONTALLY = "landscape"
    VERTICALLY = "Vertically"


def search_photo_by_keywords(keywords, orientation, is_random):
    global img
    try:
        if CLIENT_ID is None:
            raise Exception("Missing client id key.")

        url = trigger_request(orientation, keywords, is_random)

        response = requests.get(url)

        img = Image.open(BytesIO(response.content))

        if orientation == Orientation.VERTICALLY.name:
            img = img.rotate(-90, expand=True)

        print(f"Successfully found {orientation} photo with keywords '{keywords}'")

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


def trigger_request(orientation, keywords, is_random):
    if orientation == Orientation.VERTICALLY.name:
        api_orientation = 'portrait'
    else:
        api_orientation = 'landscape'
    if is_random:
        url = f"{API_HOST}/photos/random?client_id={CLIENT_ID}&orientation={api_orientation}&query={quote(str(keywords))}"
    else:
        url = f"{API_HOST}/search/photos?client_id={CLIENT_ID}&orientation={api_orientation}&query={quote(str(keywords))}"
    response = requests.get(url)
    print(url)
    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text) + 'URL:' + url)
    data = response.json()
    if is_random:
        return data["urls"]["regular"]
    else:
        return data["results"][0]["urls"]["regular"]
