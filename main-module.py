
# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from services.storage import sharedStorage

from modules.auth import *
from modules.protected import *
# from protected import *

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some_secret_key'

    # register app blueprints
    app.register_blueprint(authRoute)
    app.register_blueprint(protectedRoute)

# make sure this is turned off
@app.after_request
def attachCORSHeader(response):
    response.headers.set('Access-Control-Allow-Headers', '*')
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

# Publicly accessible routes
# ------------------------------
@app.route('/')
def home():
    output = []
    for user in sharedStorage.asList():
        output.append(str(user))
    return jsonify({
        'count': sharedStorage.totalCount(),
        'storage': output
    })


# ---------------------------------
# Server start procedure
if __name__ == '__main__':
    app.run(debug=True)
