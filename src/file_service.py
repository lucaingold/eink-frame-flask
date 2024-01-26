import os
from io import BytesIO
import base64
from PIL import Image
from flask import jsonify
from datetime import datetime
import uuid
from flask import current_app


def add_thumb_to_filename(filename):
    base, ext = os.path.splitext(filename)
    last_slash_index = base.rfind('/')
    path = base[:last_slash_index + 1] if last_slash_index != -1 else ''
    file_name = base[last_slash_index + 1:]
    new_filename = f'{path}{file_name}_thumb{ext}'
    return new_filename


class FileService:
    def __init__(self, app):
        self.static_folder = app.static_folder
        self.screen_width = current_app.config['SCREEN_WIDTH']
        self.screen_height = current_app.config['SCREEN_HEIGHT']
        pass

    def get_root_path(self):
        return current_app.config['ROOT_PATH']

    def return_image_json(self, pil_image, filename, format='JPEG'):
        image_io = BytesIO()
        pil_image.convert("RGB").save(image_io, format=format)
        image_bytes = image_io.getvalue()
        encoded_img = base64.b64encode(image_bytes).decode('ascii')
        return jsonify({'success': True, 'key': filename, "image": encoded_img})

    def save_image_and_thumbnail(self, image, filename):
        try:
            image = image.convert("RGB")
            # Save image locally with formatted name
            images_folder = os.path.join(self.static_folder, 'images', filename)
            image.save(images_folder)

            # Create and save thumbnail
            thumbnail_folder = os.path.join(self.static_folder, 'images', add_thumb_to_filename(filename))
            thumbnail_size = int(self.screen_width / 2), int(self.screen_height / 2)
            thumbnail = image.resize(thumbnail_size)
            thumbnail.save(thumbnail_folder)
        except Exception as e:
            print('Error:', str(e))
            return {'success': False, 'error': str(e)}

    def get_image_from_path(self, filename):
        try:
            image_path = os.path.join(self.static_folder, 'images', filename)
            if os.path.isfile(image_path):
                return Image.open(image_path)
            else:
                raise Exception(f'File for provided path {image_path} does not exist.')
        except Exception as e:
            raise Exception(f'Error while opening file {filename}. {e}')

    def get_all_thumbnails_from_image_folder(self):
        pictures_folder = os.path.join(self.static_folder, 'images')
        return [filename for filename in os.listdir(pictures_folder) if '_thumb.' in filename]

    def generate_file_name(self, prefix):
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%Y_%m_%d')
        unique_id = str(uuid.uuid4())[:8]  # Use the first 8 characters of the UUID
        save_filename = f"{prefix}_{formatted_date}_{unique_id}.jpeg"
        return save_filename
