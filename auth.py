# -*- coding: utf-8 -*-
from flask import Flask, Blueprint, jsonify, request, make_response
from flask import current_app
from services.tokenizer import Tokenizer
from services.storage import UserDataStorage
from models.user import User

# reference to a storage
storageProxy = UserDataStorage()

# public blueprint exposure
authRoute = Blueprint('auth', __name__)

@authRoute.route('/login')
def login():
    # get authorization field from HTTP request, early exit if it's not present
    auth = request.authorization
    if not auth:
        return make_response("HTTP Basic Authentication required 🤔", 401) #, {'WWW-Authenticate': 'Basic realm="Login required"'}

    try: # search our storage to check credentials
        username = auth.username
        password = auth.password
        storedUser = storageProxy.find(username)

        # 👇 perform validity check and password hashing 👇
        if storedUser is not None and storedUser.password == password:
            current_app.logger.info(f"<AUTH> Security check completed, passwords match.")
            # create new token using Tokenizer
            tokenService = Tokenizer(current_app.config['SECRET_KEY'])
            newToken = tokenService.createToken(username)

            utfDecodedToken = newToken.decode('UTF-8')
            current_app.logger.info(f"<AUTH> New token created.")
            return jsonify({'token': utfDecodedToken})
    except:
        make_response("Bad request parameters. Try again", 400)

    return make_response("Wrong credentials.", 401)

@authRoute.route('/logout')
def logout():
    current_app.logger.info("Someone logged out")
    # remove token from the storage
    return "You have been logged out.. But who are you ??"

@authRoute.route('/register', methods=['POST'])
def registration():
    '''
        Expecting this JSON structure in body:
        {
            'username' : "abc",
            'password': "abc",
            'email': "abc@abc"
        }
    '''
    try: #try to get the body data as JSON, fail otherwise
        body = request.json
        if body:
            username = body['username']
            pwd = body['password'] # 👇 password hashing 👇
            email = body['email']

            # add to our storage
            newUser = User(username, pwd, email)

            current_app.logger.info(f"<AUTH> Adding new user: {newUser.username}, email: {newUser.email}")
            storageProxy.store(newUser)

            return make_response("<h2>Welcome to the system</h2><br>Have a pleasant stay <strong>{}</strong> and enjoy the system :)".format(newUser.username), 201)
    except:
        current_app.logger.error("<REGISTRATION> Unable to parse POST request.")

    return make_response("Wrong parameters. Try again", 400)