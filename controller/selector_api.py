import os
from flask import Blueprint, render_template, jsonify, request
from PIL import Image


def construct_blueprint(mqtt_publisher, file_service):
    blueprint = Blueprint('selector-api', __name__, url_prefix='/selector')

    @blueprint.route('/')
    def image_selector():
        return render_template('selector.html', title='Select Image',
                               images=sorted(file_service.get_all_thumbnails_from_image_folder()))

    @blueprint.route('/load', methods=['POST'])
    def load_image_by_path():
        try:
            data = request.get_json()
            if 'path' in data:
                image_path = data['path']
                image = file_service.get_image_from_path(image_path)
                mqtt_publisher.send_image(image)
                return jsonify({'status': 'success', 'result': 'image with path' + image_path + ' processed'})
            else:
                return jsonify({'status': 'error', 'message': 'Path not provided in the request body'})
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)})

    return blueprint
