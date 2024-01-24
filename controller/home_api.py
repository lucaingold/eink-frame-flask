from flask import Blueprint
from flask import render_template, request
from flask_socketio import socketio, emit
import subprocess


def construct_blueprint(mqtt_publisher):
    blueprint = Blueprint('home-api', __name__, url_prefix='/')

    @blueprint.route('/', methods=['GET'])
    def index():
        return render_template('home.html',
                               title='E-Ink Frame',
                               status = mqtt_publisher.get_latest_device_status())

    # @socketio.on('connect')
    # def handle_connect():
    #     print('Client connected')

    return blueprint

    # @socketio.on("status")
    # def checkping():
    #     for x in range(5):
    #         cmd = 'ping -c 1 8.8.8.8|head -2|tail -1'
    #         listing1 = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, shell=True)
    #         sid = request.sid
    #         emit('server', {"data1": x, "data": listing1.stdout}, room=sid)
    #         socketio.sleep(1)
