import json
from paho.mqtt import client as mqtt_client
from data_preprocessing import fetch_pm25_data

if __name__ == '__main__':
    mqtt_ip = "192.168.0.102"
    mqtt_port = 1883
    topic = "PM2.5 data"
    msg = fetch_pm25_data()

    client = mqtt_client.Client()

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT service.")
        else:
            print("Failed to connect, return code %d\n", rc)

    client.on_connect = on_connect
    client.connect(mqtt_ip, mqtt_port)

    msg = json.dumps(msg)
    client.publish(topic, msg)
