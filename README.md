# IoT data processing simulation

This project simulates a machine learning based IoT data processing pipeline in an edge-cloud setting. A server on the edge layer collects weather data from IoT sensors located at the Newcastle's Urban Observatory and uses the MQTT protocol to send the data to another server on the edge layer (the same server in this simulation). The server then performes some data processing (removing outliers, calculating 24-hour averages) and uses the RabbitMQ protocol to send the processed data to a server on the cloud layer. That server uses the data to train a machine learning model which predicts the weather trends for the next 15 days.

![Data flow pipeline](./assets/data_flow_pipeline.png)

---

## How to run

### Edge layer setup

On a server at the **edge layer**, pull the EMQX Docker image (an MQTT platform):
```bash
docker pull emqx
```

And start the container:
```bash
docker run -d --name emqx -p 18083:18083 -p 1883:1883 emqx:latest
```

The 'docker ps' command shows a running EMQX service:

![Running EMQX container](./assets/running_emqx_container.png)

Now build a Docker image using the provided Dockerfile:
```bash
sudo docker build -t data_injector:latest . 
```

Start the container which runs the MQTT subscriber:
```bash
sudo docker-compose up
```

### Cloud layer setup

Build a Docker image from the provided Dockerfile:
```bash
sudo docker build -t data_processor:latest .
```

Start the RabbitMQ service container and data_processor container on the cloud server:
```bash
sudo docker-compose up
```

Two containers should be running on cloud:

![Cloud containers](./assets/cloud_containers.png)

Now that all the subscribers/consumers are ready and listening for messages, we can run the MQTT publisher script which initiates the process of collecting data from the IoT sensors all the way to the model training.

On the **edge layer** server, run the publisher script:
```bash
python3 mqtt_publisher.py
```

You can see the terminal outputs on the MQTT/RabbitMQ services as the data get passed along. A new folder 'output' is created in the app directory on cloud.

As a result, two new images are created on the Cloud layer in the output directory - 'Averages_over_time' and 'prediction. The former shows a graph of daily averages of weather PM2.5 data collected from the sensors and the latter shows the prediction output from the model.

![Averages over time](./assets/Averages_over_time.png)

![Predictions](./assets/prediction.png)
