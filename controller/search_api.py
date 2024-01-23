from io import BytesIO
from flask import Blueprint, render_template, jsonify, request
from PIL import Image

from src.stabilityai import Orientation
from src.unsplash import UnsplashAPI


def construct_blueprint(caching_service, mqtt_publisher, file_service):
    blueprint = Blueprint('search-api', __name__, url_prefix='/search')
    photo_api = UnsplashAPI

    @blueprint.route('/')
    def unsplash_api():
        return render_template('search.html', title='API photo search (Unsplash)', orientation_types=Orientation)

    @blueprint.route('/searchPhoto', methods=['POST'])
    def search_photo():
        try:
            data = request.json
            keywords = data.get('keywords')
            orientation = data.get('orientationType')
            is_random = data.get('isRandom')

            if not keywords:
                return jsonify({'error': 'Keywords are required'}), 400
            generated_image = photo_api.search_photo_by_keywords(keywords, orientation, is_random)
            filename = file_service.generate_file_name('photo')
            caching_service.save_image_in_cache(generated_image, filename)
            return file_service.return_image_json(generated_image, filename)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @blueprint.route('/sendToFrame', methods=['POST'])
    def send_to_frame():
        try:
            data = request.json
            key = data.get('key')
            if not key:
                return jsonify({'error': 'Key is required'}), 400
            should_save_image = data.get('should_save_image')
            cached_image = caching_service.get_image_from_cache(key)
            if cached_image:
                image = Image.open(BytesIO(cached_image))
                mqtt_publisher.send_image(image)
                if should_save_image:
                    file_service.save_image_and_thumbnail(image, key)
                return jsonify({'success': True})
        except Exception as e:
            print('Error:', str(e))
            return jsonify({'success': False, 'error': str(e)})

    return blueprint
