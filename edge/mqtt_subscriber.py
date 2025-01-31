import json
from paho.mqtt import client as mqtt_client
from data_preprocessing import calculate_24hour_average, remove_outliers
from rabbitmq_producer import send
from datetime import datetime

if __name__ == '__main__':
    mqtt_ip = "192.168.0.102"
    mqtt_port = 1883
    topic = "PM2.5 data"

    client = mqtt_client.Client()


    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Successfully connected to MQTT service.")
        else:
            print("Failed to connect, return code %d\n", rc)


    client.on_connect = on_connect
    client.connect(mqtt_ip, mqtt_port)


    def on_message(client, userdata, msg):
        msg_data = json.loads(msg.payload)

        print(f"Get message from publisher {msg_data}")

        data_wout_outliers = remove_outliers(msg_data)

        daily_averages = calculate_24hour_average(data_wout_outliers)

        send(daily_averages)


    client.subscribe(topic)
    client.on_message = on_message

    client.loop_forever()
