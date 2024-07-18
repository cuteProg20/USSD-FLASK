from flask import request, Blueprint, jsonify
from requests.auth import HTTPBasicAuth
import datetime
import base64
import requests

ussd = Blueprint('routes', __name__)

base_url = ''

def get_access_token():
    consumer_key = 'your_consumer_key'
    consumer_secret = 'your_consumer_secret'
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        r = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()  # Raise an HTTPError for bad responses
        data = r.json()
        return data['access_token']
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return None
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return None
    except ValueError as err:
        print(f"Error decoding JSON: {err}")
        return None

@ussd.route('/access_token')
def access_token_route():
    access_token = get_access_token()
    if access_token:
        return jsonify({'access_token': access_token})
    else:
        return jsonify({'error': 'Failed to retrieve access token'}), 500

@ussd.route('/register', methods=['GET'])
def registers():
    endpoint = 'http://inforwise.co.tz/broker/'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to retrieve access token'}), 500
    my_endpoint = base_url + "c2b/"
    headers = {"Authorization": "Bearer %s" % access_token}
    r_data = {
        "ShortCode": "600383",
        "ResponseType": "Completed",
        "ConfirmationURL": my_endpoint + 'con',
        "ValidationURL": my_endpoint + 'val'
    }

    response = requests.post(endpoint, json=r_data, headers=headers)
    return response.json()

@ussd.route('/simulate')
def test_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to retrieve access token'}), 500
    headers = {"Authorization": "Bearer %s" % access_token}

    data_s = {
        "Amount": 100,
        "ShortCode": "600383",
        "BillRefNumber": "test",
        "CommandID": "CustomerPayBillOnline",
        "Msisdn": "254708374149"
    }

    res = requests.post(endpoint, json=data_s, headers=headers)
    return res.json()

@ussd.route('/b2c')
def make_payment():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to retrieve access token'}), 500
    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/b2c/"

    data = {
        "InitiatorName": "testapi",
        "SecurityCredential": "your_security_credential",
        "CommandID": "BusinessPayment",
        "Amount": "200",
        "PartyA": "600981",
        "PartyB": "600981",
        "Remarks": "Pay Salary",
        "QueueTimeOutURL": my_endpoint + "timeout",
        "ResultURL": my_endpoint + "result",
        "Occasion": "Salary"
    }

    res = requests.post(endpoint, json=data, headers=headers)
    return res.json()

@ussd.route('/lnmo')
def init_stk():
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to retrieve access token'}), 500
    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/lnmo"
    Timestamp = datetime.datetime.now()
    times = Timestamp.strftime("%Y%m%d%H%M%S")
    password = "174379" + "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919" + times
    datapass = base64.b64encode(password.encode('utf-8')).decode('utf-8')

    data = {
        "BusinessShortCode": "174379",
        "Password": datapass,
        "Timestamp": times,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": "600981",
        "PartyB": "600000",
        "PhoneNumber": "255783864454",
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": 2
    }

    res = requests.post(endpoint, json=data, headers=headers)
    return res.json()

@ussd.route('/lnmo', methods=['POST'])
def lnmo_result():
    data = request.get_data()
    with open('lnmo.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return '', 204

@ussd.route('/b2c/result', methods=['POST'])
def result_b2c():
    data = request.get_data()
    with open('b2c.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return '', 204

@ussd.route('/b2c/timeout', methods=['POST'])
def b2c_timeout():
    data = request.get_data()
    with open('b2ctimeout.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return '', 204

@ussd.route('/c2b/val', methods=['POST'])
def validate():
    data = request.get_data()
    with open('data_v.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return '', 204

@ussd.route('/c2b/con', methods=['POST'])
def confirm():
    data = request.get_data()
    with open('data_c.json', 'a') as f:
        f.write(data.decode('utf-8'))
    return '', 204
