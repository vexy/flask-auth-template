
from flask import Flask, jsonify, request, make_response
from functools import wraps
from tokenizer.tokenizer import Tokenizer

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
            print("Retrieved token = " + token)
            # check for token existance
            # data = jwt.decode(token, app.config['SECRET_KEY'])

            # initialize tokenizer
            # check if we can pull out token
            tokenSupport = Tokenizer(app.config['SECRET_KEY'])
            decoded = tokenSupport.decodeToken(token)
            print("Decoded token: " + decoded)
        except:
            return jsonify({'message': 'Invalid token supplied!'}), 403
        return f(*args, **kwargs)

    return decorated

# ---------------------------------
# ROUTES DEFINITION:
@app.route('/protected')
@token_access_required
def protected():
    resp_body = jsonify({'message': 'Protected area.'})
    return resp_body

@app.route('/public')
def unprotected():
    return jsonify({'message': 'This is public domain.'})

@app.route('/login')
def login():
    # get authorization field from HTTP request
    # and early exit if it doesn't exist
    auth = request.authorization

    print("All auth fields dump")
    for k in auth:
        print("auth[" + k + "] = " + auth[k])
    if not auth:
        return make_response("Where's your token 🤔", 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    if auth.password == 'test':
        username = auth.username

        # initialize tokenizer and get token
        tokenSupport = Tokenizer(app.config['SECRET_KEY'])
        token = tokenSupport.createToken(username)

        utfDecodedToken = token.decode('UTF-8')
        return jsonify({'token': utfDecodedToken})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


# ---------------------------------
# Server start procedure
if __name__ == '__main__':
    app.run(debug=True)
