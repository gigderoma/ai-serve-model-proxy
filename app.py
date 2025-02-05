import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)



logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # INFO,  # Set the minimum level to capture (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Create handler for stdout
stdout_handler = logging.StreamHandler()  # For stdout

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
stdout_handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(stdout_handler)


@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response

# Read the environment variable
ENV = os.getenv('FLASK_ENV', 'production')  # Default to 'development' if not set

# deployed_model_name = "fraud" # Ensure that this is same as the model name you gave on OpenShift AI
# rest_url = "http://modelmesh-serving:8008" # Model Server endpoint

# Construct the inference URL for our model. Change deployed_moodel_name if you change the name of the model
infer_url = f"https://frauddetection-gig-model-frauddetection-gig.openshiftai-cluster-gig-e78f23787c77651c3692e4428c776eaa-0000.eu-gb.containers.appdomain.cloud/v2/models/frauddetection-gig-model/infer"

#Load the scaler.pkl that contained pre-trained scikit-learn scaler used to standardize or normalize input data. This ensures that the data fed into your model during inference is scaled consistently with how it was during training, improving model accuracy and performance
import pickle
with open('artifact/scaler.pkl', 'rb') as handle:
    scaler = pickle.load(handle)

# Handle the request to the model server
def rest_request(data):
    json_data = {
        "inputs": [
            {
                "name": "dense_input",
                "shape": [1, 5],
                "datatype": "FP32",
                "data": data
            }
        ]
    }

    send_data = str(json_data)
    logger.debug("sending the following data " + send_data )  # Print the data to stdout
    response = requests.post(infer_url, json=json_data)
    response_dict = response.json()
    logger.debug("received following response from model server" + response )  # Print the data to stdout
    return response_dict['outputs'][0]['data']

# Endpoint
@app.route('/', methods=['POST'])
def check_fraud():
    data = request.json
    rec_data = str(data)
    logger.debug("received the following data " + rec_data )  # Print the error message to stdout
    prediction = rest_request(scaler.transform([data]).tolist()[0]) # place a request to the model server from this service
    threshhold = 0.95
    if (prediction[0] > threshhold):
        message = 'fraud'
    else:
        message = 'not fraud'
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
