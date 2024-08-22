const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

// Load Protobuf file
const packageDef = protoLoader.loadSync('/home/tommy/Downloads/Distributed-Scalable-Data-Architecture (Protobuf)/read-service/read-service.proto', {});
const grpcObject = grpc.loadPackageDefinition(packageDef);
const readservice = grpcObject.readservice;

// Initialize the gRPC client
const client = new readservice.ReadService('localhost:50051', grpc.credentials.createInsecure());

// Express Setup
const express = require('express');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.post('/read', (req, res) => {
    const { collection, document, field } = req.body;

    // Make the gRPC request using the correct method name
    client.ReadData({ collection, document, field }, (error, response) => {
        if (error) {
            console.error('gRPC Error:', error);
            return res.status(500).send(error.message);
        }

        // Check if there is an error in the response
        if (response.error) {
            return res.status(404).json({ error: response.error });
        }

        // Deserialize the collections data
        const collections = response.collections;
        
        // Send the deserialized data as JSON response
        res.json(collections);
        console.log('Deserialized Response Collections:', collections);
    });
});

const PORT = process.env.PORT || 4001;
app.listen(PORT, () => console.log(`Read Service running on port ${PORT}`));
