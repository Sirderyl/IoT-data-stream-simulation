FROM python:3.8.12

USER root

WORKDIR /app

ADD data_preprocessing.py .
ADD mqtt_subscriber.py .
ADD rabbitmq_producer.py .
ADD requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "-u", "mqtt_subscriber.py"]