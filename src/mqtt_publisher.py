import io
import json
import os
from flask import current_app
import paho.mqtt.client as mqtt
import time


class MqttImagePublisher:

    def __init__(self, app, callback):
        self.app = app
        self.callback = callback
        self.device_status = {
            "hostname": '?',
            "ip_address": '?',
            "mac": '?',
            'status': 'unknown'
        }
        self.devices = current_app.config['DEVICES']
        self.broker_address = current_app.config['BROKER_ADDRESS']
        self.port = current_app.config['BROKER_PORT']
        self.client = mqtt.Client()
        mqtt_password = current_app.config['PASSWORD']
        if (mqtt_password):
            self.client.username_pw_set(current_app.config['USERNAME'], mqtt_password)
            self.client.tls_set()
        self.topic_send_image = current_app.config['TOPIC_IMAGE_DISPLAY']
        self.topic_status = current_app.config['TOPIC_DEVICE_STATUS']
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        print(self.broker_address + ' : ' + str(self.port))

    def connect(self):
        self.client.connect(self.broker_address, self.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(self.topic_status)
            print(f'Subscribed to {self.topic_status}')
        else:
            print(f"Connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}. Reconnecting...")
        time.sleep(5)
        self.client.reconnect()

    def on_message(self, client, userdata, msg):
        if msg.topic.endswith("/status/online"):
            device_id = msg.topic.split('/')[1]
            if device_id in self.devices:
                payload_dict = json.loads(msg.payload.decode('utf-8'))
                status_value = payload_dict.get('status', 'unknown')
                print(f"Device {device_id} is {status_value}")
                self.device_status = payload_dict
                self.callback.send(self.app, payload=payload_dict)

    def send_image(self, pil_image):
        try:
            img_byte_array = io.BytesIO()
            pil_image.convert("RGB").save(img_byte_array, format="JPEG")
            for device_id in current_app.config['DEVICES']:
                topic = self.topic_send_image.replace('+', device_id)
                self.client.publish(topic, img_byte_array.getvalue(), qos=2, retain=True)
                print(f"Image sent to {topic}")
        except Exception as e:
            print("Error sending the image:", str(e))

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def get_latest_device_status(self):
        return self.device_status
