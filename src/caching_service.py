from flask_caching import Cache
from io import BytesIO
from flask import current_app


def get_threshold():
    return int(current_app.config['CACHE_THRESHOLD_IN_SECONDS'])


class CachingService:

    def __init__(self, app):
        self.cache = Cache(app, config={'CACHE_TYPE': 'simple'})
        pass

    def get_image_from_cache(self, key):
        return self.cache.get(key)

    def save_image_in_cache(self, image, filename):
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format='JPEG')
        self.cache.set(filename, img_byte_arr.getvalue(), timeout=get_threshold())
        pass
