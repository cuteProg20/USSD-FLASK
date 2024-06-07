from flask import Flask, request
import requests
from requests.auth import HTTPBasicAuth

app = Flask(__name__)

#Third-party API urls 
THIRD_PARTY_API = "https://41.217.203.241:27443/broker/transfer"

#mpesa details
consumer_key= ''
consumer_secret= ''


@app.route('/ussd', methods=['POST'])
def ussd():
    # USSD request data
    session_id = request.form.get('sessionId')
    service_code = request.form.get('serviceCode')
    phone_number = request.form.get('phoneNumber')
    text = request.form.get('text', '')

    # Split the text input into an array of options
    text_array = text.split('*')

    response = ""

    # Initial menu
    if text == "":
        response = "CON Welcome to our USSD service\n"
        response += "1. Check Balance\n"
        response += "2. Buy Airtime\n"
    elif text == "1":
        response = "END Your balance is $10"
    elif text == "2":
        response = "CON Enter amount to buy airtime"
    elif text_array[0] == "2":
        amount = text_array[1]
        response = f"END You have successfully bought ${amount} airtime"
    else:
        response = "END Invalid input"

    return response

@app.route('/access_token')
def token():
    THIRD_PARTY_API_url= 'https://<broker-server-name-or-ip-or-address>:port/<broker-application>/b2c-request-url'

    data = (requests.get(THIRD_PARTY_API_url, HTTPBasicAuth(consumer_secret, consumer_key) ) ).json()
    return data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug = True)