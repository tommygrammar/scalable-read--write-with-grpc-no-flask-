import redis
import json
import pika
import socketio
import threading
import time
import read_service_pb2

class RedisService:
    def __init__(self, mds_host='localhost', mds_port=5006, refresh_interval=60):
        self.sio = socketio.Client()
        self.redis_address = self.get_redis_address(mds_host, mds_port)
        if not self.redis_address:
            raise Exception("Failed to retrieve Redis address from MDS")
        self.redis_client = redis.Redis(host=self.redis_address['host'], port=self.redis_address['port'], db=self.redis_address['db'])
        self.rabbitmq_host = 'localhost'
        self.mds_host = mds_host
        self.mds_port = mds_port
        self.refresh_interval = refresh_interval

        # Start a background thread to periodically refresh the Redis address
        self.refresh_thread = threading.Thread(target=self.periodic_redis_refresh, daemon=True)
        self.refresh_thread.start()

    def get_redis_address(self, mds_host, mds_port):
        # Connect to MDS
        self.sio.connect(f"http://{mds_host}:{mds_port}")

        redis_address = {}

        # Event handler to receive Redis address
        @self.sio.on('redis_address')
        def handle_response(data):
            nonlocal redis_address
            redis_address = data

        # Emit request for Redis address
        self.sio.emit('request_redis_address', {'type': 'main'})

        # Allow some time for the response
        self.sio.sleep(1)

        # Disconnect after receiving the address
        self.sio.disconnect()

        return redis_address

    def refresh_redis_client(self):
        # Get the latest Redis address
        new_redis_address = self.get_redis_address(self.mds_host, self.mds_port)
        if new_redis_address and new_redis_address != self.redis_address:
            print(f"Updating Redis address from {self.redis_address} to {new_redis_address}")
            self.redis_address = new_redis_address
            self.redis_client = redis.Redis(host=self.redis_address['host'], port=self.redis_address['port'], db=self.redis_address['db'])

    def periodic_redis_refresh(self):
        while True:
            self.refresh_redis_client()
            time.sleep(self.refresh_interval)

    def get_data(self, request):
        # Initialize a protobuf ReadResponse object
        result = read_service_pb2.ReadResponse()

        collection = request.collection
        document = request.document
        field = request.field

        # Search keys in Redis based on the collection name
        pattern = f"{collection}:*" if collection else "*"
        keys = self.redis_client.keys(pattern)

        if not keys:
            result.error = f"Collection '{collection}' does not exist."
            return result

        for key in keys:
            key_str = key.decode('utf-8')
            key_type = self.redis_client.type(key).decode('utf-8')

            if key_type == 'hash':
                key_parts = key_str.split(':')
                if len(key_parts) < 2:
                    continue

                collection_name = key_parts[0]
                doc_name = key_parts[1]

                if document and document != doc_name:
                    continue

                if collection and collection_name != collection:
                    continue

                # Get or create the collection in the response
                collection_entry = result.collections[collection_name]
                # Get or create the document within the collection
                document_entry = collection_entry.documents[doc_name]

                fields = self.redis_client.hgetall(key)

                if field:
                    if field in fields:
                        document_entry.fields[field] = fields[field]
                    else:
                        result.error = f"Field '{field}' does not exist in document '{doc_name}'."
                        return result
                else:
                    for k, v in fields.items():
                        document_entry.fields[k] = v
            else:
                print(f"Skipping key {key_str} of type {key_type}")
        print("the result is", result)

        return result

    def on_request(self, ch, method, props, body):
        try:
            # Log the received message
            print(f"Received raw body: {body}")

            # Decode the incoming protobuf payload
            request = read_service_pb2.ReadRequest()
            request.ParseFromString(body)  # Deserialize from binary

            # Log the parsed request
            print(f"Parsed Request: {request}")

            # Process the request using the get_data method
            response = self.get_data(request)
            print("response after redis befor serialization", response)

            # Encode the response as a protobuf payload
            response_data = response.SerializeToString()

            print("response _data after being serialized", response_data)

            # Send the response back
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=response_data
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            print(f"Error processing request: {e}")
            ch.basic_nack(delivery_tag=method.delivery_tag)

    def start_service(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue='read_queue')

        channel.basic_consume(queue='read_queue', on_message_callback=self.on_request)

        print(" [x] Awaiting RPC requests")
        channel.start_consuming()

if __name__ == "__main__":
    rds = RedisService()
    rds.start_service()
