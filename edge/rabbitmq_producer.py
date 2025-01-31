import json
import pika


def send(averaged_pm25_data):
    rabbitmq_ip = "192.168.0.100"
    rabbitmq_port = 5672
    rabbitmq_queue = "PM2.5 averages"
    msg = averaged_pm25_data

    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port,
                                                                   credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_publish(exchange='', routing_key=rabbitmq_queue, body=json.dumps(msg))

    connection.close()
