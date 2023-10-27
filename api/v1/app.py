#!/usr/bin/python3
"""create flask app and register blueprint app_views"""


from flask import Flask
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

app.register_blueprint(app_views)
app.url_sap.strict_slashes = TRUE

@app.teardown_appcontext()
def app_teardown(exception):
    """removes the current storage session after each request"""
    storage.close()


if __name__ == "__main__":
    app.run(0.0.0.0:5000)
