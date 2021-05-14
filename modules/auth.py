# -*- coding: utf-8 -*-
from flask import Flask, Blueprint
from flask import jsonify, request, make_response
from flask import current_app
from services.tokenizer import Tokenizer
from services.storage import sharedStorage
from models.user import User

# public blueprint exposure
authRoute = Blueprint('auth', __name__)

# 👇 implement your strategy here 👇
@authRoute.route('/login', methods=['POST'])
def login():
    # get authorization field from HTTP request, early exit if it's not present
    auth = request.authorization
    if not auth:
        return make_response("HTTP Basic Authentication required 🤔", 401) #, {'WWW-Authenticate': 'Basic realm="Login required"'}

    try: # search our storage to check credentials
        username = auth.username
        password = auth.password
        storedUser = sharedStorage.find(username)

        # 👇 implement your strategy here 👇
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

# 👇 implement your strategy here 👇
@authRoute.route('/logout')
def logout():
    current_app.logger.info("Someone logged out")
    # eg. remove/invalidate token from our storage
    return "You have been logged out.. But who are you ??"

# 👇 implement your strategy here 👇
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
            pwd = body['password']
            email = body['email']

            # add to our storage
            # 👈 add password hashing strategy here before saving to DB
            newUser = User(username, pwd, email)

            current_app.logger.info(f"<AUTH> Adding new user: {newUser.username}, email: {newUser.email}")
            sharedStorage.store(newUser)

            return make_response("<h2>Welcome to the system</h2><br>Have a pleasant stay <strong>{}</strong> and enjoy the system :)".format(newUser.username), 201)
    except:
        current_app.logger.error("<REGISTRATION> Unable to parse POST request.")

    return make_response("Wrong parameters. Try again", 400)
