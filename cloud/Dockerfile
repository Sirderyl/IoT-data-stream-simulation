FROM python:3.8.12

USER root

WORKDIR /app

ADD rabbitmq_consumer.py .
ADD requirements.txt .
ADD ml_engine.py .
ADD pm25_prediction.py .

RUN pip install -r requirements.txt

RUN mkdir -p /app/output

CMD ["python3", "-u", "rabbitmq_consumer.py"]