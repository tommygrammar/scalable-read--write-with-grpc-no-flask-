from concurrent import futures
import grpc
import read_service_pb2
import read_service_pb2_grpc
import pika
import uuid
import json

rabbitmq_host = 'localhost'

# gRPC Service Implementation
class ReadServiceServicer(read_service_pb2_grpc.ReadServiceServicer):
    def ReadData(self, request, context):
        # Prepare the payload
        payload = {
            'collection': request.collection,
            'document': request.document,
            'field': request.field
        }
        
        correlation_id, response_queue = self.send_to_rabbitmq(payload)
        read_response = self.receive_from_rabbitmq(correlation_id, response_queue)

        print("the response is:", read_response)
        
        # Handle the result
        if read_response:
            return read_response
        else:
            return read_service_pb2.ReadResponse(error="No data received")

    def send_to_rabbitmq(self, payload):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue='read_queue')

        # Convert the payload into the ReadRequest Protobuf message
        read_request = read_service_pb2.ReadRequest(
            collection=payload['collection'],
            document=payload['document'],
            field=payload['field']
        )

        # Serialize the message to a binary format
        message = read_request.SerializeToString()

        print(message)

        # Generate a unique correlation ID for this request
        correlation_id = str(uuid.uuid4())
        response_queue = 'response_queue_' + correlation_id

        # Declare a unique response queue
        channel.queue_declare(queue=response_queue)

        # Publish the message to the RabbitMQ read_queue
        channel.basic_publish(
            exchange='',
            routing_key='read_queue',
            body=message,
            properties=pika.BasicProperties(
                reply_to=response_queue,
                correlation_id=correlation_id
            )
        )

        # Close the connection
        connection.close()

        return correlation_id, response_queue

    def receive_from_rabbitmq(self, correlation_id, response_queue):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()
        
        # Declare the response queue
        channel.queue_declare(queue=response_queue)
        
        response = None  # Initialize as None to handle the protobuf binary data

        def on_response(ch, method, properties, body):
            if properties.correlation_id == correlation_id:
                nonlocal response
                response = body  # Store the raw protobuf binary data
                ch.basic_ack(delivery_tag=method.delivery_tag)
                ch.stop_consuming()
        
        channel.basic_consume(queue=response_queue, on_message_callback=on_response)
        channel.start_consuming()
        
        # Cleanup the response queue after consumption
        channel.queue_delete(queue=response_queue)
        connection.close()
        
        print("This is the raw protobuf response:", response)

        if response:
            read_response = read_service_pb2.ReadResponse()
            read_response.ParseFromString(response)

        print("this is the deserialized", read_response)

        
        
        return read_response  # Return the raw protobuf binary data

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    read_service_pb2_grpc.add_ReadServiceServicer_to_server(ReadServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
