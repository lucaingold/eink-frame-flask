from flask import Flask, render_template
import os

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


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080)
    app.run(host="192.168.0.20", port=5000, debug=True)