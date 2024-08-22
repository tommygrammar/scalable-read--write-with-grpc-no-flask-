from concurrent import futures
import grpc
import write_service_pb2
import write_service_pb2_grpc
import pika
import uuid

# gRPC Service Implementation
class WriteServiceServicer(write_service_pb2_grpc.WriteServiceServicer):
    def WriteData(self, request, context):
        try:
            # Convert ScalarMapContainer to a standard Python dictionary
            fields_dict = dict(request.fields)

            # Prepare the payload based on the incoming gRPC request
            payload = {
                'collection': request.collection,
                'document': request.document,
                'fields': fields_dict
            }

            print("This is the write payload", payload)

            # Convert the request to a Protobuf message for RabbitMQ
            write_request = write_service_pb2.WriteRequest(
                collection=request.collection,
                document=request.document,
                fields=fields_dict
            )

            # Serialize the Protobuf message to bytes
            serialized_message = write_request.SerializeToString()

            # Send the serialized Protobuf message to RabbitMQ
            response = self.send_to_rabbitmq(serialized_message)

            # Handle the result
            if response == "success":
                return write_service_pb2.WriteResponse(message="Data successfully queued for writing.")
            else:
                return write_service_pb2.WriteResponse(error="Failed to queue data.")
        except Exception as e:
            print(f"Exception in WriteData: {e}")
            return write_service_pb2.WriteResponse(error="Internal server error")

    def send_to_rabbitmq(self, request):
        try:
            # Create a connection to RabbitMQ
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()

            # Declare the queue
            channel.queue_declare(queue='write_queue', durable=True)

            # Check if request is already in byte format
            if isinstance(request, bytes):
                message = request
            else:
                # Serialize the Protobuf message to bytes
                message = request.SerializeToString()

            print("This is the serialized write payload:", message)

            # Generate a correlation ID
            correlation_id = str(uuid.uuid4())

            # Publish the message to RabbitMQ
            channel.basic_publish(
                exchange='',
                routing_key='write_queue',
                body=message,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Make the message persistent
                    correlation_id=correlation_id
                )
            )

            # Close the connection
            connection.close()

            return "success"
        except Exception as e:
            print(f"Error sending data to RabbitMQ: {e}")
            return "error"

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    write_service_pb2_grpc.add_WriteServiceServicer_to_server(WriteServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("gRPC Write Service running on port 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
