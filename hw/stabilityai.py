import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
import requests
from enum import Enum

DISPLAY_TYPE = "waveshare_epd.it8951"
ENGINE_ID = "stable-diffusion-v1-6"
# API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')
API_HOST = 'https://api.stability.ai'
API_KEY = 'sk-S05RrvORkvGgWnE2wg952awDz7bJIdkWKjCAHpz8mIx5VvOY'


class ArtType(Enum):
    NONE = ""
    _3D_MODEL = "3d-model"
    ANALOG_FILM = "analog-film"
    ANIME = "anime"
    CINEMATIC = "cinematic"
    COMIC_BOOK = "comic-book"
    DIGITAL_ART = "digital-art"
    ENHANCE = "enhance"
    FANTASY_ART = "fantasy-art"
    ISOMETRIC = "isometric"
    LINE_ART = "line-art"
    LOW_POLY = "low-poly"
    MODELING_COMPOUND = "modeling-compound"
    NEON_PUNK = "neon-punk"
    ORIGAMI = "origami"
    PHOTOGRAPHIC = "photographic"
    PIXEL_ART = "pixel-art"
    TILE_TEXTURE = "tile-texture"


def get_image_from_string(prompt, art_type):
    global img
    try:
        fetch_height = 1152
        fetch_width = 1536

        if API_KEY is None:
            raise Exception("Missing Stability API key.")

        payload = generate_style_preset_payload(prompt, art_type, fetch_height, fetch_width)

        response = requests.post(
            f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            },
            json=payload,
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()

        print(str('successful generated image with prompt' + prompt))

        for i, image in enumerate(data["artifacts"]):
            img = Image.open(BytesIO(base64.b64decode(image["base64"])))

        img = img.resize((1600, 1200))
        # img.resize((1600, 1200))
        return img
    except BaseException as e:
        logging.error(e)
        return None


def generate_style_preset_payload(prompt, art_type, fetch_height, fetch_width):
    # Check if art_type is NONE and conditionally generate style_preset
    style_preset = None if art_type == ArtType.NONE else art_type.value

    # Construct the JSON payload
    payload = {
        "text_prompts": [
            {
                "text": prompt + ' . in grayscale and bright background.'
            }
        ],
        "cfg_scale": 7,
        "height": fetch_height,
        "width": fetch_width,
        "samples": 1,
        "style_preset": art_type,
        "steps": 30,
    }

    # Include style_preset in the payload only if it's not NONE
    if style_preset is not None:
        payload["style_preset"] = style_preset

    return payload
