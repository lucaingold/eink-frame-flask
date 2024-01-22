import base64
import io

import paho.mqtt.client as mqtt
import time


class MqttImagePublisher:
    def __init__(self, broker_address, topic_to_send_image_to, port=1883):
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.topic = topic_to_send_image_to

    def connect(self):
        self.client.connect(self.broker_address, self.port)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
        else:
            print(f"Connection failed with code {rc}")

    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code {rc}. Reconnecting...")
        time.sleep(5)
        self.connect()

    def send_image(self, pil_image):
        try:
            img_byte_array = io.BytesIO()
            pil_image.save(img_byte_array, format="JPEG")
            self.client.publish(self.topic, img_byte_array.getvalue(), qos=1)
            print(f"Image sent to {self.topic}")
        except Exception as e:
            print("Error sending the image:", str(e))

    def start(self):
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
