from io import BytesIO

from PIL.Image import Resampling
from flask import Flask, render_template, jsonify, request
import os

from hw.frame import EInkFrame
from PIL import Image, ImageOps

file_path = os.getcwd()

frameInstance = EInkFrame()
frameInstance.run()

app = Flask(__name__)

@app.route('/')
def image_selector():
    pictures_folder = os.path.join(app.static_folder, 'pictures')
    pictures_paths = [os.path.join('pictures', filename) for filename in os.listdir(pictures_folder) if filename.endswith(('.jpeg'))]
    return render_template('selector.html', title='Select Image', images=sorted(pictures_paths))


@app.route('/upload')
def image_upload():
    return render_template('upload.html',title='Upload Image')


@app.route('/ai')
def ai_generator():
    return render_template('ai.html',title='Ai Generator (Stable Diffusion)')


@app.route('/api')
def unsplash_api():
    return render_template('api.html',title='API Search (Unslash)')


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

    # Use ImageOps.exif_transpose to handle image orientation
    if original_image.width < original_image.height:
        original_image = original_image.transpose(method=Image.Transpose.ROTATE_90)


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
    return jsonify({'status': 'success', 'result': 'image processed'})

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
                return jsonify({'status': 'error', 'message': 'File for provided path ' + image_path + ' does not exist.'})
        else:
            return jsonify({'status': 'error', 'message': 'Path not provided in the request body'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)