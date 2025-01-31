import json
import pika
from pm25_prediction import collect, save_chart, predict

if __name__ == '__main__':
    rabbitmq_ip = "192.168.0.100"
    rabbitmq_port = 5672
    rabbitmq_queue = "PM2.5 averages"

    def callback(ch, method, properties, body):
        msg = json.loads(body)

        pm25_df = collect(msg)
        save_chart(pm25_df)
        predict(pm25_df)

    # RabbitMQ connection with timeout of 1 minute
    credentials = pika.PlainCredentials('user', 'password')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=rabbitmq_ip, port=rabbitmq_port, socket_timeout=60, credentials=credentials)
    )

    channel = connection.channel()

    # Queue
    channel.queue_declare(queue=rabbitmq_queue)
    channel.basic_consume(queue=rabbitmq_queue, auto_ack=True, on_message_callback=callback)
    channel.start_consuming()
