import logging
from io import BytesIO
from PIL import Image
import base64
import requests
from enum import Enum
from flask import current_app


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


class StabilityAI:
    def __init__(self):
        self.api_key = current_app.config['AI_API_KEY']
        self.api_host = current_app.config['AI_API_HOST']
        self.api_cfg_scale = current_app.config['CFG_SCALE']
        self.screen_width = current_app.config['SCREEN_WIDTH']
        self.screen_height = current_app.config['SCREEN_HEIGHT']
        self.screen_aspect_ratio = float(current_app.config['SCREEN_ASPECT_RATIO'])
        pass

    def get_image_from_string(self, positive_prompt, negative_prompt, art_type, engine_type, orientation):
        global img
        try:
            fetch_width, fetch_height = set_fetch_dimensions(engine_type, orientation)
            if self.api_key is None:
                raise Exception("Missing Stability API key.")

            payload = self.generate_style_preset_payload(positive_prompt, negative_prompt, art_type, fetch_height,
                                                    fetch_width)
            print(str(payload))
            data = self.trigger_request(engine_type, payload)
            # data = None
            print(
                f"Successfully generated {orientation} image with positive prompt '{positive_prompt}' [{engine_type}, {art_type}, {negative_prompt}]")

            for i, image in enumerate(data["artifacts"]):
                img = Image.open(BytesIO(base64.b64decode(image["base64"])))

            if orientation == Orientation.VERTICALLY.name:
                img = img.rotate(-90, expand=True)

            img = self.crop_to_aspect_ratio_and_resize(img)

            return img
        except BaseException as e:
            logging.error(e)
            return None

    def crop_to_aspect_ratio_and_resize(self, image):
        width, height = image.size
        current_aspect_ratio = height / width
        target_aspect_ratio = self.screen_aspect_ratio

        if current_aspect_ratio > target_aspect_ratio:
            new_height = int(width * target_aspect_ratio)
            top = (height - new_height) // 2
            bottom = top + new_height
            cropped_image = image.crop((0, top, width, bottom))
        elif current_aspect_ratio < target_aspect_ratio:
            # Crop the width to achieve the target aspect ratio
            new_width = int(height / target_aspect_ratio)
            left = (width - new_width) // 2
            right = left + new_width
            cropped_image = image.crop((left, 0, right, height))
        else:
            # The aspect ratio is already correct, no need to crop
            cropped_image = image
        new_width, new_height = image.size
        print(f"New width: {new_width} , new height: {new_height}")
        return cropped_image.resize((self.screen_width, self.screen_height))

    def trigger_request(self, engine_type, payload):
        response = requests.post(
            f"{self.api_host}/v1/generation/{engine_type}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            json=payload,
        )
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))
        data = response.json()
        return data

    def list_engines(self):
        if self.api_key is None:
            raise Exception("Missing Stability API key.")
        payload = {}
        headers = {
            'Accept': 'application/json',
            "Authorization": f"Bearer {self.api_key}"
        }
        url = f"{self.api_host}/v1/engines/list"
        print(url)
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code == 200:
            data = response.json()
            picture_items = [item for item in data if item["type"] == "PICTURE"]
            id_description_mapping = {item["id"]: item["description"] for item in picture_items}
            return id_description_mapping
        else:
            print(f"Error: {response.status_code} , Description: {response.reason}")

    def generate_style_preset_payload(self, positive_prompt, negative_prompt, art_type, fetch_height, fetch_width):
        payload = {
            "text_prompts": [
                {
                    "text": positive_prompt,
                    "weight": 1
                }
            ],
            "cfg_scale": self.api_cfg_scale,
            "height": fetch_height,
            "width": fetch_width,
            "samples": 1,
            "steps": 30,
        }

        if negative_prompt and negative_prompt.strip():
            payload["text_prompts"].append({
                "text": negative_prompt,
                "weight": -1
            })

        if art_type and art_type in ArtType.__members__ and ArtType[art_type] is not ArtType.NONE:
            payload["style_preset"] = ArtType[art_type].value

        return payload
