from flask import Flask, request
# import requests
# from requests.auth import HTTPBasicAuth

app = Flask(__name__)

#Third-party API urls 
THIRD_PARTY_API_URL = "https://41.217.203.241:27443/broker/transfer"


cusumer_key = ''
cunsumer_secrete = ''

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
       #Call the third-party API
       api_response = request.get(THIRD_PARTY_API_URL)
       if api_response.status_code==200:
           data = api_response.json()

        # Assuming the api returns json repose with a 'message' field
       api_message = data.get('message', 'No data found')
       response = f"END {api_message}"
    else:
        response = "END Invalid input"

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug = True)