
# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request, make_response
from functools import wraps
from services.tokenizer import Tokenizer
from services.storage import UserDataStorage
from models.user import User

# initialize in memory token storage
ds = UserDataStorage()
usr = UserDataStorage()


# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)

# used as part of your authentication strategy
app.config['SECRET_KEY'] = 'some_secret_key'

# protector function wraping other functions
def token_access_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #get token from URL

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            # make sure we can decode token
            tokenSupport = Tokenizer(app.config['SECRET_KEY'])
            decoded = tokenSupport.decodeToken(token)
        except:
            return jsonify({'message': 'Invalid token supplied!'}), 401
        return f(*args, **kwargs)

    return decorated



# ROUTES DEFINITION:
# ---------------------------------
@app.route('/protected')
@token_access_required
def protected():
    resp_body = jsonify({'message': 'Welcome to protected area, you made it'})
    return resp_body

# Publicly accessible
# ---------------------------------
@app.route('/')
def home():
    return jsonify({'message': 'This is root of the domain. Public area'})

@app.route('/login')
def login():
    # get authorization field from HTTP request, early exit if it's not present
    auth = request.authorization
    if not auth:
        return make_response("HTTP Basic Authentication required 🤔", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    try: # search our storage to check credentials
        username = auth.username
        password = auth.password
        storedUser = ds.getData(username)

        # 👇 perform validity check and password hashing 👇
        if storedUser is not None and storedUser.password == password:
            # create new token using Tokenizer
            tokenSupport = Tokenizer(app.config['SECRET_KEY'])
            newToken = tokenSupport.createToken(username)

            utfDecodedToken = newToken.decode('UTF-8')
            return jsonify({'token': utfDecodedToken})
    except:
        make_response("Bad request parameters. Try again", 400)

    return make_response("Credentials don't match. Try again", 401)

@app.route('/register', methods=['POST'])
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
        app.logger.info("Received: " + str(body))
        if body:
            username = body['username']
            pwd = body['password'] # 👇 password hashing 👇
            email = body['email']

            # add to our storage
            newUser = User(username, pwd, email)

            app.logger.info("New user registered: " + newUser.username + "email: " + newUser.email)
            ds.store(newUser)

            return make_response("Welcome <strong>{}</strong>. Have a pleasant stay".format(username), 201)
    except:
        app.logger.info("Unable to parse POST")

    return make_response("Wrong parameters. Try again", 400)


# ---------------------------------
# Server start procedure
if __name__ == '__main__':
    app.run(debug=True)
