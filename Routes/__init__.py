from flask import Flask

def ussd_app():
    app = Flask(__name__)
    
    from Routes.routes import routes as ussd_blueprint

    app.register_blueprint(ussd_blueprint, url_prefix = '/register')