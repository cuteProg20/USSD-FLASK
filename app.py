from flask import Flask
from Routes.routes import ussd

app = Flask(__name__)

customer_key = ''
customer_secrets = ''

THIRD_PARTY_API_URL = "https://41.217.203.241:27443/broker/transfer"

# Register the Blueprint
app.register_blueprint(ussd)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
