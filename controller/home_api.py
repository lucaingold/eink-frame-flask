from flask import Blueprint, send_file
from flask import render_template, request
from flask_socketio import socketio, emit
import subprocess


def construct_blueprint(mqtt_publisher):
    blueprint = Blueprint('home-api', __name__, url_prefix='/')

    @blueprint.route('/', methods=['GET'])
    def index():
        return render_template('home.html',
                               title='E-Ink Frame',
                               status=mqtt_publisher.get_latest_device_status())

    @blueprint.route('/manifest.json', methods=['GET'])
    def serve_manifest():
        return send_file('manifest.json', mimetype='application/manifest+json')

    @blueprint.route('/sw.js', methods=['GET'])
    def serve_sw():
        return send_file('sw.js', mimetype='application/javascript')

    return blueprint
