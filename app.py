from flask import Flask, render_template, jsonify, request
import os

from hw.frame import EInkFrame
from PIL import Image

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
    app.run(host='0.0.0.0', port=8080)
    # app.run(host="192.168.0.20", port=5000, debug=True)