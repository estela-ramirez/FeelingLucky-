import smartcar
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)

# global variable to save our access_token
access = None


# TODO: Authorization Step 1a: Launch Smartcar authorization dialog
client = smartcar.AuthClient(
    client_id='36794b07-4dc7-47cf-9502-b9061100c093',
    client_secret='d0db6b8f-b828-43f7-8711-3bacd5d1c8f8',
    redirect_uri='http://localhost:8000/exchange',
    scope=['read_vehicle_info'],
    test_mode=False,
)

@app.route('/', methods=['GET'])
def login():
    auth_url = client.get_auth_url()
    return redirect(auth_url)   #redirects client to this url to authenticate


@app.route('/exchange', methods=['GET'])
def exchange():
    # TODO: Authorization Step 3: Handle Smartcar response

    # TODO: Request Step 1: Obtain an access token

    code = request.args.get('code')  #code is token

    global access
    # in a production app you'll want to store this in some kind of
    # persistent storage
    access = client.exchange_code(code)
    return '', 200


@app.route('/vehicle', methods=['GET'])
def vehicle():

    # TODO: Request Step 2: Get vehicle ids

    #data = json.loads(json_data)

    # TODO: Request Step 3: Create a vehicle

    # TODO: Request Step 4: Make a request to Smartcar API

    global access
    # the list of vehicle ids
    vehicle_ids = smartcar.get_vehicle_ids(
        access['access_token'])['vehicles']

    vehicle = smartcar.Vehicle(vehicle_ids[0], access['access_token'])

    info = vehicle.info()
    #lock = vehicle.unlock()
    print(info)
    '''
    {
        "id": "36ab27d0-fd9d-4455-823a-ce30af709ffc",
        "make": "TESLA",
        "model": "Model S",
        "year": 2014
    }
    '''

    return jsonify(info)


if __name__ == '__main__':
    app.run(port=8000)
