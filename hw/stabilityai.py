import logging
from PIL import Image, ImageDraw, ImageFont, PngImagePlugin
from pip._vendor.six import BytesIO
import base64
import requests

DISPLAY_TYPE = "waveshare_epd.it8951"
ENGINE_ID = "stable-diffusion-v1-6"
# API_HOST = os.getenv('API_HOST', 'https://api.stability.ai')
API_HOST = 'https://api.stability.ai'
API_KEY = 'sk-S05RrvORkvGgWnE2wg952awDz7bJIdkWKjCAHpz8mIx5VvOY'


def get_image_from_string(prompt):
    global img
    try:
        fetch_height = 1280
        fetch_width = 1600

        # fetch_height = 512
        # fetch_width = 512

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

        print(str('successful generated image with prompt' + prompt))

        for i, image in enumerate(data["artifacts"]):
            img = Image.open(BytesIO(base64.b64decode(image["base64"])))

        img = img.crop((1600, 1200))
        # img.resize((1600, 1200))
        return img
    except BaseException as e:
        logging.error(e)
        return None