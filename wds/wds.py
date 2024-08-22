import redis
import pika
import write_service_pb2

class WriteDistributionService:
    def __init__(self):
        self.redis_client1 = redis.Redis(host='localhost', port=6379, db=0)
        self.redis_client2 = redis.Redis(host='localhost', port=6380, db=0)

        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='write_queue', durable=True)

    def write_data(self, collection, document, fields):
        try:
            for field, content in fields.items():
                if content is not None:
                    self.redis_client1.hset(f"{collection}:{document}", field, content)
                    
            return "success"
        except Exception as e:
            print(f"Error writing to Redis: {e}")
            return "error"

    def callback(self, ch, method, properties, body):
        try:
            # Deserialize the Protobuf message
            write_request = write_service_pb2.WriteRequest()
            write_request.ParseFromString(body)

            # Extract data from the Protobuf message
            collection = write_request.collection
            document = write_request.document

            # Handle the map fields
            fields = {key: value for key, value in write_request.fields.items()}

            print(f"Collection: {collection}, Document: {document}, Fields: {fields}")

            # Write the data to Redis
            response = self.write_data(collection, document, fields)

            if response == "success":
                ch.basic_ack(delivery_tag=method.delivery_tag)
            else:
                print("Failed to write data to Redis")
        except Exception as e:
            print(f"Error in callback: {e}")

    def consume_queue(self):
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='write_queue', on_message_callback=self.callback)
        print('Waiting for messages...')
        self.channel.start_consuming()

if __name__ == "__main__":
    wds = WriteDistributionService()
    wds.consume_queue()
