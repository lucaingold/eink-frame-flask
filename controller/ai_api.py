from io import BytesIO
from flask import Blueprint, render_template, jsonify, request
from PIL import Image
from src.stabilityai import ArtType, Orientation, StabilityAI


def construct_blueprint(caching_service, mqtt_publisher, file_service):
    blueprint = Blueprint('ai-api', __name__, url_prefix='/ai')
    ai_api = StabilityAI()

    @blueprint.route('/')
    def ai_generator():
        return render_template('ai.html',
                               title='Ai Generator (Stable Diffusion)',
                               status=mqtt_publisher.get_latest_device_status(),
                               art_types=ArtType,
                               engines=ai_api.list_engines(),
                               orientation_types=Orientation)

    @blueprint.route('/generate', methods=['POST'])
    def generate_ai_image():
        try:
            data = request.json
            positive_prompt = data.get('positive_prompt')
            negative_prompt = data.get('negative_prompt')
            art_type = data.get('artType')
            engine_type = data.get('engineType')
            orientation = data.get('orientationType')

            if not positive_prompt:
                return jsonify({'error': 'Prompt is required'}), 400

            generated_image = ai_api.get_image_from_string(positive_prompt, negative_prompt, art_type, engine_type,
                                                           orientation)
            filename = file_service.generate_file_name('ai')
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
            raise Exception("Generated image not in cache")
        except Exception as e:
            print('Error:', str(e))
            return jsonify({'success': False, 'error': str(e)})

    return blueprint
