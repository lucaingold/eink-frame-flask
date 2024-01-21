import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
import requests
from enum import Enum

DISPLAY_TYPE = "waveshare_epd.it8951"
ENGINE_ID = "stable-diffusion-xl-beta-v2-2-2"
CFG_SCALE = 7
API_HOST = 'https://api.stability.ai'
API_KEY = 'sk-S05RrvORkvGgWnE2wg952awDz7bJIdkWKjCAHpz8mIx5VvOY'


class Orientation(Enum):
    HORIZONTALLY = "Horizontally"
    VERTICALLY = "Vertically"


class ArtType(Enum):
    NONE = "none"
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


def get_image_from_string(prompt, art_type, engine_type, orientation):
    global img
    try:

        if orientation == Orientation.HORIZONTALLY.value:
            fetch_width = 1024
            fetch_height = 768
        else:
            fetch_width = 768
            fetch_height = 1024

        if API_KEY is None:
            raise Exception("Missing Stability API key.")

        payload = generate_style_preset_payload(prompt, art_type, fetch_height, fetch_width)
        data = trigger_request(engine_type, payload, prompt)

        for i, image in enumerate(data["artifacts"]):
            img = Image.open(BytesIO(base64.b64decode(image["base64"])))

        if orientation == Orientation.HORIZONTALLY.value:
            img = img.rotate(90, expand=True)

        img = img.resize((1600, 1200))
        return img
    except BaseException as e:
        logging.error(e)
        return None


def trigger_request(engine_type, payload, prompt):
    response = requests.post(
        f"{API_HOST}/v1/generation/{engine_type}/text-to-image",
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
    return data


def list_engines():
    if API_KEY is None:
        raise Exception("Missing Stability API key.")
    payload = {}
    headers = {
        'Accept': 'application/json',
        "Authorization": f"Bearer {API_KEY}"
    }
    url = f"{API_HOST}/v1/engines/list"
    response = requests.request("GET", url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        picture_items = [item for item in data if item["type"] == "PICTURE"]
        id_description_mapping = {item["id"]: item["description"] for item in picture_items}
        return id_description_mapping
    else:
        print(f"Error: {response.status_code} , Description: {response.reason}")


def generate_style_preset_payload(prompt, art_type, fetch_height, fetch_width):
    # Check if art_type is NONE and conditionally generate style_preset
    if isinstance(art_type, ArtType):
        style_preset = None if art_type == ArtType.NONE else art_type.value
    else:
        style_preset = None  # Handle the case where art_type is not an instance of ArtType

    # Construct the JSON payload
    payload = {
        "text_prompts": [
            {
                "text": prompt
            }
        ],
        "cfg_scale": CFG_SCALE,
        "height": fetch_height,
        "width": fetch_width,
        "samples": 1,
        "steps": 30,
    }

    # Include style_preset in the payload only if it's not NONE
    if style_preset is not None:
        payload["style_preset"] = style_preset

    return payload
