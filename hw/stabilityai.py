import logging
from io import BytesIO

from PIL import Image
import base64
import requests
from enum import Enum

DISPLAY_TYPE = "waveshare_epd.it8951"
ENGINE_ID = "stable-diffusion-xl-beta-v2-2-2"
CFG_SCALE = 7
API_HOST = 'https://api.stability.ai'
API_KEY = 'sk-S05RrvORkvGgWnE2wg952awDz7bJIdkWKjCAHpz8mIx5VvOY'
TARGET_ASPECT_RATIO = 3 / 4
SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1200


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
        fetch_width, fetch_height = set_fetch_dimensions(engine_type, orientation)

        if API_KEY is None:
            raise Exception("Missing Stability API key.")

        payload = generate_style_preset_payload(prompt, art_type, fetch_height, fetch_width)
        print(str(payload))
        data = trigger_request(engine_type, payload, prompt)
        # data = None
        print(f"Successfully generated {orientation} image with prompt '{prompt}' [{engine_type}, {art_type}]")

        for i, image in enumerate(data["artifacts"]):
            img = Image.open(BytesIO(base64.b64decode(image["base64"])))

        if orientation == Orientation.VERTICALLY.name:
            img = img.rotate(-90, expand=True)

        img = crop_to_aspect_ratio_and_resize(img)

        return img
    except BaseException as e:
        logging.error(e)
        return None


def set_fetch_dimensions(engine_type, orientation):
    if engine_type in ["stable-diffusion-xl-1024-v0-9", "stable-diffusion-xl-1024-v1-0"]:
        fetch_width, fetch_height = 1216, 832
    elif engine_type == "stable-diffusion-xl-beta-v2-2-2":
        fetch_width, fetch_height = 704, 512
    else:
        fetch_width, fetch_height = 1024, 768
    if orientation == Orientation.VERTICALLY.name:
        fetch_width, fetch_height = fetch_height, fetch_width

    return fetch_width, fetch_height


def crop_to_aspect_ratio_and_resize(image):
    width, height = image.size
    current_aspect_ratio = height / width

    if current_aspect_ratio > TARGET_ASPECT_RATIO:
        new_height = int(width * TARGET_ASPECT_RATIO)
        top = (height - new_height) // 2
        bottom = top + new_height
        cropped_image = image.crop((0, top, width, bottom))
    elif current_aspect_ratio < TARGET_ASPECT_RATIO:
        # Crop the width to achieve the target aspect ratio
        new_width = int(height / TARGET_ASPECT_RATIO)
        left = (width - new_width) // 2
        right = left + new_width
        cropped_image = image.crop((left, 0, right, height))
    else:
        # The aspect ratio is already correct, no need to crop
        cropped_image = image
    new_width, new_height = image.size
    print(f"New width: {new_width} , new height: {new_height}")
    return cropped_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))


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

    if art_type and art_type in ArtType.__members__ and ArtType[art_type] is not ArtType.NONE:
        payload["style_preset"] = ArtType[art_type].value

    return payload
