import pika  # Import the Pika library, which allows interaction with RabbitMQ
from pika.exchange_type import ExchangeType  # Import ExchangeType for defining the type of exchange

# Define the connection parameters for RabbitMQ server on localhost
connection_parameters = pika.ConnectionParameters('localhost')

# Establish a connection to the RabbitMQ server
connection = pika.BlockingConnection(connection_parameters)

# Create a communication channel
channel = connection.channel()

# Declare a topic exchange named 'topic'
channel.exchange_declare(exchange='topic', exchange_type=ExchangeType.topic)

# Define a message for user payments
user_payments_message = 'A european user paid for something'

# Publish the user payments message to the 'topic' exchange with a specific routing key
channel.basic_publish(exchange='topic', routing_key='user.europe.payments', body=user_payments_message)

# Print a confirmation message to the console for the user payments message
print(f'sent message: {user_payments_message}')

# Define a message for business orders
business_order_message = 'A european business ordered goods'

# Publish the business order message to the 'topic' exchange with a specific routing key
channel.basic_publish(exchange='topic', routing_key='business.europe.order', body=business_order_message)

# Print a confirmation message to the console for the business order message
print(f'sent message: {business_order_message}')

# Close the connection to the RabbitMQ server
connection.close()
