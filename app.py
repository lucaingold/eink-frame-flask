from flask import Flask
from src.file_service import FileService
from src.mqtt_publisher import MqttImagePublisher
from src.caching_service import CachingService
from controller.ai_api import construct_blueprint as ai_api
from controller.home_api import construct_blueprint as home_api
from controller.load_url_api import construct_blueprint as load_from_url_api
from controller.mandelbrot_api import construct_blueprint as mandelbrot_api
from controller.search_api import construct_blueprint as search_api
from controller.selector_api import construct_blueprint as selector_api
from controller.upload_api import construct_blueprint as upload_api
import configparser


def create_app():
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read('config.ini')
    load_config(config, app)
    return app


def load_config(config, app):
    # MQTT
    app.config['BROKER_ADDRESS'] = config.get('MQTT', 'BROKER_ADDRESS')
    app.config['USERNAME'] = config.get('MQTT', 'USERNAME')
    app.config['PASSWORD'] = config.get('MQTT', 'PASSWORD')
    app.config['TOPIC_IMAGE_DISPLAY'] = config.get('MQTT', 'TOPIC_IMAGE_DISPLAY')
    app.config['BROKER_PORT'] = config.get('MQTT', 'BROKER_PORT')
    # App
    app.config['CACHE_THRESHOLD_IN_SECONDS'] = config.get('APP', 'CACHE_THRESHOLD_IN_SECONDS')
    # Screen
    app.config['SCREEN_WIDTH'] = config.get('SCREEN', 'WIDTH')
    app.config['SCREEN_HEIGHT'] = config.get('SCREEN', 'HEIGHT')
    app.config['SCREEN_ASPECT_RATIO'] = config.get('SCREEN', 'ASPECT_RATIO')
    # AI
    app.config['CFG_SCALE'] = config.get('STABILITY_AI', 'CFG_SCALE')
    app.config['AI_API_HOST'] = config.get('STABILITY_AI', 'API_HOST')
    app.config['AI_API_KEY'] = config.get('STABILITY_AI', 'API_KEY')
    # Unsplash
    app.config['PHOTO_API_HOST'] = config.get('PHOTO_API', 'API_HOST')
    app.config['PHOTO_CLIENT_ID'] = config.get('PHOTO_API', 'CLIENT_ID')


def init_mqtt():
    publisher = MqttImagePublisher()
    publisher.connect()
    publisher.start()
    return publisher


def register_blueprints():
    app.register_blueprint(ai_api(caching_service, mqtt_publisher, file_service))
    app.register_blueprint(home_api())
    app.register_blueprint(load_from_url_api(mqtt_publisher))
    app.register_blueprint(mandelbrot_api(mqtt_publisher, file_service))
    app.register_blueprint(search_api(caching_service, mqtt_publisher, file_service))
    app.register_blueprint(selector_api(mqtt_publisher, file_service))
    app.register_blueprint(upload_api(mqtt_publisher, file_service))


app = create_app()
app.app_context().push()
mqtt_publisher = init_mqtt()
caching_service = CachingService(app)
file_service = FileService(app)
register_blueprints()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
