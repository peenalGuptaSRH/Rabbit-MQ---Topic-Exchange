import pika  # Import the Pika library, which allows interaction with RabbitMQ
from pika.exchange_type import ExchangeType  # Import ExchangeType to specify the type of exchange

# Define a callback function to handle messages received
def on_message_received(ch, method, properties, body):
    print(f'Analytics - received new message: {body}')

# Set connection parameters to connect to the RabbitMQ server on localhost
connection_parameters = pika.ConnectionParameters('localhost')

# Establish a blocking connection to the RabbitMQ server
connection = pika.BlockingConnection(connection_parameters)

# Create a communication channel
channel = connection.channel()

# Declare a topic exchange named 'topic'. This creates the exchange if it does not already exist.
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

# Declare a temporary, exclusive queue. This creates a queue with a unique name that will be deleted when the connection is closed.
queue = channel.queue_declare(queue='analytics_queue', exclusive=True)

# Bind the queue to the 'topic' exchange with a routing key pattern. This routing key pattern will match messages with keys like '*.europe.*'.
channel.queue_bind(exchange='topic', queue=queue.method.queue, routing_key='*.europe.*')

# Set up subscription on the declared queue. Whenever a message is received, the on_message_received callback function is called.
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

# Print a message to indicate that the consumer is starting
print('Analytics Starting Consuming')

# Start consuming messages from the queue
channel.start_consuming()
