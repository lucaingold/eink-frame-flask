import base64
import os
import json
import uuid
from datetime import datetime
from io import BytesIO
from time import sleep

from flask import Flask, render_template, jsonify, request, send_file
from PIL import Image, ExifTags
from hw.image_by_url import show_from_url
from hw.mandelbrot import create_mandelbrot_image
from hw.stabilityai import get_image_from_string, ArtType, list_engines, Orientation
from hw.unsplash import search_photo_by_keywords
from flask_caching import Cache
from hw.frame import EInkFrame
# from hw.frameMock import EInkFrameMock

THREE_MINUTES = 180

file_path = os.getcwd()

frameInstance = EInkFrame()
# frameInstance = EInkFrameMock()

frameInstance.run()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})


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


@app.route('/mandelbrot')
def mandelbrot():
    return render_template('mandelbrot.html', title='Mandelbrot Set')


@app.route('/url')
def load_by_url():
    return render_template('url.html', title='Show by url', orientation_types=Orientation)


@app.route('/generateAiImage', methods=['POST'])
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

        generated_image = get_image_from_string(positive_prompt, negative_prompt, art_type, engine_type, orientation)
        # frameInstance.display_image_on_epd(generated_image)
        filename = generate_file_name('ai')
        save_image_in_cache(generated_image, filename)
        return return_image_json(generated_image, filename)
    except Exception as e:
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
        # frameInstance.display_image_on_epd(generated_image)
        filename = generate_file_name('photo')
        save_image_in_cache(generated_image, filename)
        return return_image_json(generated_image, filename)
    except Exception as e:
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

    return jsonify({'success': True})


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


@app.route('/calculateMandelbrotImage')
def calculate_mandelbrot_image():
    try:
        mandelbrot_img = create_mandelbrot_image()
        frameInstance.display_image_on_epd(mandelbrot_img)
        return return_image_json(mandelbrot_img)
    except Exception as e:
        # Handle exceptions as needed
        return jsonify({'error': str(e)}), 500


@app.route('/loadImage', methods=['POST'])
def load_image_from_url():
    try:
        data = request.json
        url = data.get('url')
        orientation = data.get('orientationType')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        img = show_from_url(url, orientation)
        frameInstance.display_image_on_epd(img)

        return jsonify({'success': True})

    except Exception as e:
        # Handle exceptions as needed
        return jsonify({'error': str(e)}), 500


@app.route('/sendToFrame', methods=['POST'])
def send_to_frame():
    try:
        data = request.json
        key = data.get('key')
        if not key:
            return jsonify({'error': 'Key is required'}), 400
        should_save_image = data.get('should_save_image')
        cached_image = cache.get(key)
        if cached_image:
            image = Image.open(BytesIO(cached_image))
            frameInstance.display_image_on_epd(image)
            if should_save_image:
                save_image_and_thumbnail(image, key)
            return jsonify({'success': True})
    except Exception as e:
        print('Error:', str(e))
        return jsonify({'success': False, 'error': str(e)})


def save_image_and_thumbnail(image, filename):
    try:
        # Save image locally with formatted name
        images_folder = os.path.join(app.static_folder, 'images', filename)
        image.save(images_folder)

        # Create and save thumbnail
        thumbnail_folder = os.path.join(app.static_folder, 'pictures', filename)
        thumbnail_size = (1000, 750)
        thumbnail = image.resize(thumbnail_size)
        thumbnail.save(thumbnail_folder)
    except Exception as e:
        print('Error:', str(e))
        return {'success': False, 'error': str(e)}


def generate_file_name(prefix):
    current_datetime = datetime.now()
    formatted_date = current_datetime.strftime('%Y_%m_%d')
    unique_id = str(uuid.uuid4())[:8]  # Use the first 8 characters of the UUID
    save_filename = f"{prefix}_{formatted_date}_{unique_id}.jpeg"
    return save_filename


def return_image_json(pil_image, filename, format='JPEG'):
    image_io = BytesIO()
    pil_image.save(image_io, format=format)
    image_bytes = image_io.getvalue()
    encoded_img = base64.b64encode(image_bytes).decode('ascii')
    return jsonify({'success': True, 'key': filename, "image": encoded_img})


def save_image_in_cache(image, filename):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='JPEG')
    cache.set(filename, img_byte_arr.getvalue(), timeout=THREE_MINUTES)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # app.run(host='0.0.0.0', port=8080, debug=False)
