from flask import Flask, jsonify, request, make_response
import jwt
import datetime

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)

app.config['SECRET_KEY'] = 'some_secret_key'

# ROUTES DEFINITION:
@app.route('/unprotected')
def unprotected():
    return 'This is unprotected area'

@app.route('/protected')
def protected():
    return 'This is protected area'

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
