const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const path = require('path');

// Load the proto file
const PROTO_PATH = path.join('/home/tommy/Downloads/Distributed-Scalable-Data-Architecture (Protobuf)/write-service/write-service.proto');
const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true
});

const grpcObject = grpc.loadPackageDefinition(packageDefinition);

// Check the structure of grpcObject
console.log('grpcObject:', grpcObject);

// Access WriteService properly
const WriteService = grpcObject.WriteService;  // or grpcObject.write.WriteService

// Initialize the gRPC client
const client = new WriteService('localhost:50052', grpc.credentials.createInsecure());

const express = require('express');
const cors = require('cors');

// Express Setup
const app = express();
app.use(cors());
app.use(express.json());

/**
 * Sends a write request to the gRPC server.
 * @param {string} collection - The collection name.
 * @param {string} document - The document name.
 * @param {Object} fields - The fields to write as key-value pairs.
 */
function sendWriteRequest(collection, document, fields, res) {
    // Ensure the fields are passed correctly as a map
    const requestPayload = {
      collection,
      document,
      fields // No need to transform this into an array if it’s already an object with key-value pairs
    };

    console.log(requestPayload)
  
    // Make the gRPC request using the correct method name
    client.WriteData(requestPayload, (error, response) => {
      if (error) {
        console.log('gRPC Error:', error);
        return res.status(500).send(error.message);
      }
  
      // Check if there is an error in the response
      if (response.error) {
        return res.status(500).json({ error: response.error });
      }
  
      // Send the successful response message
      res.json({ message: response.message });
      console.log('Write request successful:', response.message);
    });
  }
  
// API endpoint for handling write requests
app.post('/write', (req, res) => {
  const { collection, document, fields } = req.body;

  // Validate input
  if (!collection || !document || !fields) {
    return res.status(400).json({ error: 'Missing required fields: collection, document, or fields' });
  }

  // Call the write function
  sendWriteRequest(collection, document, fields, res);
});

const PORT = process.env.PORT || 4002;
app.listen(PORT, () => console.log(`Write Service running on port ${PORT}`));
