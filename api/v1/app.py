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

#task 5
# error handler for 404
@app.errorhandler(404)
def not_found(error):
    """ Return json response for 404 not found message"""
    response = ('error': 'Not found')
    return jsonify(response), 404


if __name__ == "__main__":
    # get host and post from environment variables
    HOST = getenv('HBNB_API_HOST', '0.0.0.0')
    PORT = int (getenv('HBNB_API_PORT', 5000))
    app.run(0.0.0.0:5000)
    # run app in threaded mode
    app.run(host=HOST, port=PORT, threaded=True)
