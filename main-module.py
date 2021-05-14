
# -*- coding: utf-8 -*-
from services.mongodb import Database
from flask import Flask, Blueprint

# services.* are used as DB hooks below
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
    # register DB routes later

# make sure this is turned or configured according to your needs
@app.after_request
def attachCORSHeader(response):
    response.headers.set('Access-Control-Allow-Headers', '*')
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

# Publicly accessible routes
# ------------------------------
@app.route('/')
def home():
    # This route returns a JSON of "users in the system"
    # Replace it with your own logic
    output = []
    for user in sharedStorage.asList():
        output.append(str(user))
    return jsonify({
        'count': sharedStorage.totalCount(),
        'storage': output
    })

# Publicly accessible routes with DB support
# ------------------------------
@app.route('/mongo_db')
def mongo_db():
    from services.mongodb import Database

    # This route returns a list of data from a "User" collection
    # it assumes having valid MongoDB connection
    # Replace it with your own logic
    mongoClient = Database("localhost", "user", "pwd")

    output = []
    output = mongoClient.filter("mainCollection", "{'name': 'someName'}")

    # format JSON response
    response = jsonify({'results': output}) 
    return response

@app.route('/sql_db')
def mongo_db():
    from services.mysql import Database

    # This route returns a list of data from a "User" collection
    # it assumes having valid MongoDB connection
    # Replace it with your own logic
    sqlClient = Database()

    output = []
    output = sqlClient.filter("someTable", "user123")

    # format JSON response
    response = jsonify({'results': output}) 
    return response

# ---------------------------------
# Server start procedure
if __name__ == '__main__':
    app.run(debug=True)
