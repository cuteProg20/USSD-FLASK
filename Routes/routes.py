from flask import request, Blueprint, jsonify
from requests.auth import HTTPBasicAuth
import datetime
import base64
import requests

ussd = Blueprint('routes', __name__)

base_url = ''

def get_access_token():
    consumer_key = 'UfELfLvSlWmxhgRoUA5Ef2Oz5z3k7vHLT5GA4m4D8WFI9877'
    consumer_secret = 'EcocavejjYr6xKpA2YssFTQuEGa6wS5Cr1N1cMvFP92fFcupQO6jW31MuKESSG50'
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
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
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
    endpoint = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest'
    access_token = get_access_token()
    if not access_token:
        return jsonify({'error': 'Failed to retrieve access token'}), 500
    headers = {"Authorization": "Bearer %s" % access_token}
    my_endpoint = base_url + "/b2c/"

    data = {
    "OriginatorConversationID": "6b43c5e1-5fb1-4665-af47-9dcf52659d19",
    "InitiatorName": "testapi",
    "SecurityCredential": "n1Kui3rZvk50R7ELjfVdbDP0X5xZ5wHnp/Cnbdx43VJSA+LQEKeEP5+MfeTAN9wrkTiCprE6MRAfDhS0BtNt0WSoVFeP5x7Stu4FQ2bl7BCNiApPL90qyBF6cNLBl/jb1fGLrgbs3IT/CUiaCTjVyncQknsASzyNE/vD5Ru/8/mQQ3IE3levgLb6Y3yaSdeu8XwP7XZNJPDkui9GdMAuueHpWz8z6vsAKQ4HKo/2IzDNPeEsheMMeUj260avqM/lHiABktGF3lFm3Ibt3gOWZLvpgdbqXyq+sUNZmFc48EeVOmq3BL4x3dll/3U3+SsOsa2f9EIANh6/vTmuYwDjUg==",
    "CommandID": "BusinessPayment",
    "Amount": 10,
    "PartyA": 600997,
    "PartyB": 254708374149,
    "Remarks": "Test remarks",
    "QueueTimeOutURL": "https://mydomain.com/b2c/queue",
    "ResultURL": "https://mydomain.com/b2c/result",
    "Occasion": "",
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
