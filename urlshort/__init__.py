from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = 'kljdh33939393k3fjkh3h3h3h'

    from . import urlshort
    app.register_blueprint(urlshort.bp)

    return app