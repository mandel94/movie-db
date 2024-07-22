# Dockerfile.rabbitmq

# Use the official RabbitMQ image as a base
FROM rabbitmq:3-management

# Enable the required RabbitMQ plugins
RUN rabbitmq-plugins enable --offline rabbitmq_mqtt rabbitmq_federation_management rabbitmq_stomp


