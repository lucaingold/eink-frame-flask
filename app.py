from io import BytesIO

from PIL.Image import Resampling
from flask import Flask, render_template, jsonify, request, send_file
import os
import json

from hw.frame import EInkFrame
# from hw.frameMock import EInkFrameMock
from PIL import Image, ImageOps, ExifTags

from hw.stabilityai import get_image_from_string, ArtType, list_engines, Orientation
from hw.unsplash import search_photo_by_keywords

file_path = os.getcwd()

frameInstance = EInkFrame()
# frameInstance = EInkFrameMock()
frameInstance.run()

app = Flask(__name__)


@app.route('/')
def image_selector():
    pictures_folder = os.path.join(app.static_folder, 'pictures')
    pictures_paths = [os.path.join('pictures', filename) for filename in os.listdir(pictures_folder) if
                      filename.endswith(('.jpeg'))]
    return render_template('selector.html', title='Select Image', images=sorted(pictures_paths))


@app.route('/upload')
def image_upload():
    return render_template('upload.html', title='Upload Image')


@app.route('/ai')
def ai_generator():
    return render_template('ai.html', title='Ai Generator (Stable Diffusion)', art_types=ArtType,
                           engines=list_engines(), orientation_types=Orientation)


@app.route('/api')
def unsplash_api():
    return render_template('api.html', title='API photo search (Unsplash)', orientation_types=Orientation)


@app.route('/generateAiImage', methods=['POST'])
def generateAiImage():
    try:
        data = request.json
        prompt = data.get('prompt')
        art_type = data.get('artType')
        engine_type = data.get('engineType')
        orientation = data.get('orientationType')

        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400

        generated_image = get_image_from_string(prompt, art_type, engine_type, orientation)
        frameInstance.display_image_on_epd(generated_image)

        return jsonify({'success': True})
    except Exception as e:
        # Handle exceptions as needed
        return jsonify({'error': str(e)}), 500


@app.route('/searchPhoto', methods=['POST'])
def search_photo():
    try:
        data = request.json
        keywords = data.get('keywords')
        orientation = data.get('orientationType')
        is_random = data.get('isRandom')

        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        generated_image = search_photo_by_keywords(keywords, orientation, is_random)
        frameInstance.display_image_on_epd(generated_image)

        return jsonify({'success': True})
    except Exception as e:
        # Handle exceptions as needed
        return jsonify({'error': str(e)}), 500


@app.route('/uploadImage', methods=['POST'])
def upload():
    # Access the file from the request
    uploaded_file = request.files['file']
    if uploaded_file:
        # Read the image using PIL
        try:
            original_image = Image.open(uploaded_file)
            ow = str(original_image.width)
            oh = str(original_image.height)
            print(' h:' + oh)
            print(' w:' + ow)
            # Resize the image to 1600x1200
            # target_width = 1600
            # target_height = 1200
            # resized_image = original_image.resize((target_width, target_height))
            #
            # orientation = get_orientation(original_image)
            #
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

            frameInstance.display_image_on_epd(original_image)
        except Exception as e:
            return jsonify({'error': 'Failed to process image'}), 500
        return json.dumps({'status': 'success', 'message': 'File uploaded successfully' + ' h:' + oh + ' w:' + ow})
    else:
        return json.dumps({'status': 'error', 'message': 'No file received'})


@app.route('/sendImage', methods=['POST'])
def send_image():
    # Check if the request contains a file
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    # Get the image file from the request
    image_file = request.files['image']

    # Read the image using PIL
    try:
        original_image = Image.open(image_file)
    except Exception as e:
        return jsonify({'error': 'Failed to process image'}), 500

    ow = str(original_image.width)
    oh = str(original_image.height)

    orientation = get_orientation(original_image)

    if orientation:
        # Use EXIF orientation information
        if orientation == 3:
            original_image = original_image.transpose(method=Image.Transpose.ROTATE_180)
        elif orientation == 6:
            original_image = original_image.transpose(method=Image.Transpose.ROTATE_270)
        elif orientation == 8:
            original_image = original_image.transpose(method=Image.Transpose.ROTATE_90)
        # Additional cases can be added based on the specific orientation values
    else:
        # If no EXIF information, use width < height condition
        if original_image.width < original_image.height:
            original_image = original_image.transpose(method=Image.Transpose.ROTATE_270)

    # Resize the image to 1600x1200
    target_width = 1600
    target_height = 1200
    resized_image = original_image.resize((target_width, target_height))

    # If the image needs to be cropped to the exact dimensions
    # you can add additional logic here based on your requirements

    # Convert the image to BMP format
    bmp_image = resized_image.convert('RGB')

    # Save the BMP image to a BytesIO object
    bmp_buffer = BytesIO()
    bmp_image.save(bmp_buffer, format='BMP')

    frameInstance.display_image_on_epd(bmp_image)

    # Return the BMP image bytes as the response
    #     return jsonify({'status': 'success', 'result': 'image processed' + 'W: ' + oh + ' H: ' + ow})
    # return jsonify({'message': 'BMP image processed successfully ' + 'W: ' + oh + ' H: ' + ow,
    #                 'bmp_image': bmp_buffer.getvalue().decode('latin-1')})

    return send_file(BytesIO(bmp_buffer.getvalue()), mimetype='image/bmp', as_attachment=True,
                     download_name='processed_image.bmp')


def get_orientation(image):
    # Check if image has EXIF orientation information
    try:
        for tag, value in image._getexif().items():
            if ExifTags.TAGS.get(tag) == 'Orientation':
                return value
    except (AttributeError, KeyError, TypeError, IndexError):
        pass

    return None


@app.route('/load', methods=['POST'])
def load_image_by_path():
    try:
        data = request.get_json()
        if 'path' in data:
            image_path = data['path']
            if os.path.isfile(image_path):
                pil_image = Image.open(image_path)
                frameInstance.display_image_on_epd(pil_image)
                return jsonify({'status': 'success', 'result': 'image with path' + image_path + ' processed'})
            else:
                return jsonify(
                    {'status': 'error', 'message': 'File for provided path ' + image_path + ' does not exist.'})
        else:
            return jsonify({'status': 'error', 'message': 'Path not provided in the request body'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
