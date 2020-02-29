from flask import Flask, jsonify, request, make_response
import jwt
import datetime
from functools import wraps

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'some_secret_key'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') #get token from URL

        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Invalid token supplied!'}), 403
        return f(*args, **kwargs)

    return decorated

# ROUTES DEFINITION:
@app.route('/unprotected')
def unprotected():
    return jsonify({'message': 'Anyone can view this!'})

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'Protected area'})

@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == 'password':
        token_expiration = str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
        token = jwt.encode(
        {
            'user': auth.username,
            'expiration': token_expiration
        }, app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})

# start the server
if __name__ == '__main__':
    app.run(debug=True)
