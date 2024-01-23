from flask import Blueprint, render_template, jsonify
from src.mandelbrot import create_mandelbrot_image


def construct_blueprint(mqtt_publisher, file_service):
    blueprint = Blueprint('mandelbrot-api', __name__, url_prefix='/mandelbrot')

    @blueprint.route('/')
    def mandelbrot():
        return render_template('mandelbrot.html', title='Mandelbrot Set')

    @blueprint.route('/calculate')
    def calculate_mandelbrot_image():
        try:
            original_image = create_mandelbrot_image()
            mqtt_publisher.send_image(original_image)
            return file_service.return_image_json(original_image)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return blueprint
