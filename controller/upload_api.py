import json
from flask import Blueprint, render_template, jsonify, request
from PIL import Image


def construct_blueprint(mqtt_publisher, file_service):
    blueprint = Blueprint('upload-api', __name__, url_prefix='/upload')

    @blueprint.route('/')
    def image_upload():
        return render_template('upload.html',
                               status=mqtt_publisher.get_latest_device_status(),
                               title='Upload Image')

    @blueprint.route('/upload', methods=['POST'])
    def upload():
        uploaded_file = request.files['file']
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                # Resize the image
                # target_width =
                # target_height =
                # resized_image = original_image.resize((target_width, target_height))
                #
                # orientation = get_orientation(original_image)
                # if orientation:
                #     # Use EXIF orientation information
                #     if orientation == 3:
                #         resized_image = resized_image.transpose(method=Image.Transpose.ROTATE_180)
                #     elif orientation == 6:
                #         resized_image = resized_image.transpose(method=Image.Transpose.ROTATE_270)
                #     elif orientation == 8:
                #         resized_image = resized_image.transpose(method=Image.Transpose.ROTATE_90)
                #     # Additional cases can be added based on the specific orientation values
                # else:
                #     # If no EXIF information, use width < height condition
                #     if resized_image.width < resized_image.height:
                #         resized_image = resized_image.transpose(method=Image.Transpose.ROTATE_270)

                # hf = request.data
                should_save_image = request.args.get('shouldSaveImage')
                if should_save_image is not None and should_save_image.lower() == 'true':
                    file_service.save_image_and_thumbnail(image, file_service.generate_file_name('upload'))
                mqtt_publisher.send_image(image)
            except Exception as e:
                return jsonify({'error': f'Failed to process image {str(e)}'}), 500
            return json.dumps({'status': 'success', 'message': 'File uploaded successfully'}), 200
        else:
            return json.dumps({'status': 'error', 'message': 'No file received'}), 500

    return blueprint
