import logging
import os
from omni_epd import displayfactory, EPDNotFoundError
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
from hw.file_operations import FileOperations
from hw.image_functions import ImageFunctions
from constants import ConfigConst
from hw.config_wrapper import Configs
from flask import requests

DISPLAY_TYPE = "waveshare_epd.it8951"
ENGINE_ID = "stable-diffusion-v1-6"
# API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')
API_HOST = 'https://api.stability.ai'
API_KEY = 'sk-S05RrvORkvGgWnE2wg952awDz7bJIdkWKjCAHpz8mIx5VvOY'


def get_image_from_string(prompt):
    global img
    try:
        fetch_height = 1200
        fetch_width = 1600

        if API_KEY is None:
            raise Exception("Missing Stability API key.")
        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": fetch_height,
                "width": fetch_width,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        for i, image in enumerate(data["artifacts"]):
            img = Image.open(BytesIO(base64.b64decode(image["base64"])))
        return img
    except BaseException as e:
        logging.error(e)
        return None