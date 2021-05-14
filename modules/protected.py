# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask import jsonify, request, make_response
from flask import current_app

from services.tokenizer import Tokenizer
from services.storage import sharedStorage  # CONNECT WITH DIFFERENT DB SERVICES HERE

from models.user import User    # REPLACE WITH YOUR OWN MODELS IF NEEDED
from functools import wraps

# public blueprint exposure
protectedRoute = Blueprint('protected', __name__)

# protector function wraping other functions
def token_access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') # get token from URL

        if not token:
            return jsonify({'message': 'Protected area. Valid access token required'}), 403
        try: # make sure we can decode token
            tokenSupport = Tokenizer(current_app.config['SECRET_KEY'])
            decodedUser = tokenSupport.decodeToken(token)['user']
            # and that we have a storage entry for this user
            storedUser = sharedStorage.find(decodedUser)
            if storedUser and storedUser.username == decodedUser:
                current_app.logger.info(f"<PROTECTED_ACCESS> Username pair matches, protected entry allowed.")
            else:
                return jsonify({'message': 'Invalid access token supplied.'}), 401
        except:
            return jsonify({'message': 'Invalid access token supplied.'}), 401
        return f(*args, **kwargs)

    return decorated

# Protected ROUTES DEFINITION:  (split further to standalone Blueprints)
# -----------------------------
@protectedRoute.route('/protected1')
@token_access_required
def protected():
    resp_body = jsonify({'message': 'Welcome to protected area 1, you made it'})
    return resp_body

@protectedRoute.route('/protected2')
@token_access_required
def protected2():
    resp_body = jsonify({'message': 'Welcome to protected area 2, you made it'})
    return resp_body
