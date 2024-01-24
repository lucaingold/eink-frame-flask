from PIL import Image
from flask import Blueprint, render_template, jsonify


def construct_blueprint(mqtt_publisher, file_service):
    blueprint = Blueprint('mandelbrot-api', __name__, url_prefix='/mandelbrot')

    @blueprint.route('/')
    def mandelbrot():
        return render_template('mandelbrot.html', title='Mandelbrot Set')

    @blueprint.route('/calculate')
    def calculate_mandelbrot_image():
        try:
            size = (1600, 1200)
            extent = (-2, -2, 2, 2)
            quality = 128
            mandelbrot = Image.effect_mandelbrot(size, extent, quality)
            mqtt_publisher.send_image(mandelbrot)
            return file_service.return_image_json(mandelbrot, 'mandelbrot')
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return blueprint
