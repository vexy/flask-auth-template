
# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, jsonify, request, make_response
from functools import wraps
from services.tokenizer import Tokenizer
from services.storage import UserDataStorage
from models.user import User
from auth import *

# initialize in memory user data storage
centralStorage = None

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)
    # used as part of your authentication strategy
    app.config['SECRET_KEY'] = 'some_secret_key'
    # register auth blueprint
    app.register_blueprint(authRoute)

# protector function wraping other functions
def token_access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #get token from URL

        if not token:
            return jsonify({'message': 'Protected area. Valid access token required'}), 403
        try: # make sure we can decode token
            tokenSupport = Tokenizer(app.config['SECRET_KEY'])
            decodedUser = tokenSupport.decodeToken(token)['user']
            # and that we have a storage entry for this user
            storedUser = storageProxy.find(decodedUser)
            if storedUser and storedUser.username == decodedUser:
                app.logger.info(f"<PROTECTED_ACCESS> Username pair matches, protected entry allowed.")
            else:
                return jsonify({'message': 'Invalid access token supplied.'}), 401
        except:
            return jsonify({'message': 'Invalid access token supplied.'}), 401
        return f(*args, **kwargs)

    return decorated



# ROUTES DEFINITION:
# ---------------------------------
@app.route('/protected')
@token_access_required
def protected():
    # TODO unpack user
    resp_body = jsonify({'message': 'Welcome to protected area, you made it'})
    return resp_body

# Publicly accessible
# ---------------------------------
@app.route('/')
def home():
    output = []
    for user in storageProxy.asList():
        output.append(str(user))
    return jsonify({
        'count': storageProxy.totalCount(),
        'storage': output
    })


# ---------------------------------
# Server start procedure
if __name__ == '__main__':
    app.run(debug=True)
