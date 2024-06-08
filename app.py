from flask import Flask, request
from app import app
app = Flask(__name__)


customer_key = ''
customer_secrets = ''

#Third-party API urls 
THIRD_PARTY_API_URL = "https://41.217.203.241:27443/broker/transfer"




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("3000"), debug = True)