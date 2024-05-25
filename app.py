# from flask import Flask
# app = Flask (__name__)

# @app.route("/")
# def home():
#     return "{\"message\":\"Hey there am python flask\"}"

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=int("3000"), debug = True)

from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug = True)