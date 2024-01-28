from flask import Blueprint, render_template, jsonify, request
from src.image_by_url import ImageByUrl
from src.stabilityai import Orientation


def construct_blueprint(mqtt_publisher, file_service):
    blueprint = Blueprint('url-api', __name__, url_prefix='/url')

    @blueprint.route('/')
    def load_by_url():
        return render_template('url.html',
                               title='Show by url',
                               status=mqtt_publisher.get_latest_device_status(),
                               orientation_types=Orientation)

    @blueprint.route('/load', methods=['POST'])
    def load_image_from_url():
        try:
            data = request.json
            url = data.get('url')
            orientation = data.get('orientationType')
            should_save_image = data.get('should_save_image')
            if not url:
                return jsonify({'error': 'URL is required'}), 400
            original_image = ImageByUrl().show_from_url(url, orientation)
            mqtt_publisher.send_image(original_image)
            if should_save_image:
                file_service.save_image_and_thumbnail(original_image, file_service.generate_file_name('url'))
            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return blueprint
