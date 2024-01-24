from time import sleep

import socketio
from flask import Flask
from flask_socketio import SocketIO, emit

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
from blinker import Namespace


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
    app.config['TOPIC_DEVICE_STATUS'] = config.get('MQTT', 'TOPIC_DEVICE_STATUS')
    app.config['BROKER_PORT'] = config.getint('MQTT', 'BROKER_PORT')
    # Devices
    app.config['DEVICES'] = list(map(str.strip, config.get('DEVICES', 'LIST').split(',')))
    # App
    app.config['CACHE_THRESHOLD_IN_SECONDS'] = config.getint('APP', 'CACHE_THRESHOLD_IN_SECONDS')
    # Screen
    app.config['SCREEN_WIDTH'] = config.getint('SCREEN', 'WIDTH')
    app.config['SCREEN_HEIGHT'] = config.getint('SCREEN', 'HEIGHT')
    app.config['SCREEN_ASPECT_RATIO'] = config.getfloat('SCREEN', 'ASPECT_RATIO')
    # AI
    app.config['CFG_SCALE'] = config.getint('STABILITY_AI', 'CFG_SCALE')
    app.config['AI_API_HOST'] = config.get('STABILITY_AI', 'API_HOST')
    app.config['AI_API_KEY'] = config.get('STABILITY_AI', 'API_KEY')
    # Unsplash
    app.config['PHOTO_API_HOST'] = config.get('PHOTO_API', 'API_HOST')
    app.config['PHOTO_CLIENT_ID'] = config.get('PHOTO_API', 'CLIENT_ID')


def init_mqtt(callback):
    publisher = MqttImagePublisher(app, callback)
    publisher.connect()
    publisher.start()
    return publisher


def register_blueprints():
    app.register_blueprint(ai_api(caching_service, mqtt_publisher, file_service))
    app.register_blueprint(home_api(mqtt_publisher))
    app.register_blueprint(load_from_url_api(mqtt_publisher))
    app.register_blueprint(mandelbrot_api(mqtt_publisher, file_service))
    app.register_blueprint(search_api(caching_service, mqtt_publisher, file_service))
    app.register_blueprint(selector_api(mqtt_publisher, file_service))
    app.register_blueprint(upload_api(mqtt_publisher, file_service))


app = create_app()
app.app_context().push()


def device_status_changed(app, payload, **extra):
    socketio.emit('device_status_changed', payload)


socketio = SocketIO(app, logger=True)
signals_namespace = Namespace()
callback_device_status_changed = signals_namespace.signal('callback_device_status_changed')
callback_device_status_changed.connect(device_status_changed, app)
mqtt_publisher = init_mqtt(callback_device_status_changed)

caching_service = CachingService(app)
file_service = FileService(app)
register_blueprints()

if __name__ == '__main__':
    app.debug = True
    socketio.run(app, host='0.0.0.0', debug=True)
    while True:
        emit('device_status_changed', {'text': 'Message received!'})
        sleep(6)
