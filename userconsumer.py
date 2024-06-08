import pika  # Import the Pika library for interacting with RabbitMQ
from pika.exchange_type import ExchangeType  # Import the ExchangeType for specifying the exchange type

# Define a callback function to handle messages received from the queue
def on_message_received(ch, method, properties, body):
    print(f'User - received new message: {body}')

# Define connection parameters to connect to RabbitMQ server on localhost
connection_parameters = pika.ConnectionParameters('localhost')

# Establish a blocking connection to the RabbitMQ server
connection = pika.BlockingConnection(connection_parameters)

# Create a communication channel
channel = connection.channel()

# Declare an exchange of type 'topic' named 'topic'
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

# Declare a temporary queue with a random name. 'exclusive=True' means the queue will be deleted when the connection closes.
queue = channel.queue_declare(queue='', exclusive=True)

# Bind the queue to the 'topic' exchange with a routing key pattern 'user.#'
channel.queue_bind(exchange='topic', queue=queue.method.queue, routing_key='user.#')

# Set up subscription on the queue. The on_message_received function will be called whenever a message is received.
channel.basic_consume(queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received)

# Print a message to indicate that the consumer is starting
print('User Starting Consuming')

# Start consuming messages from the queue
channel.start_consuming()
