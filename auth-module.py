from flask import Flask

# initialize main Flask object
if __name__ == '__main__':
    app = Flask(__name__)

# ROUTES DEFINITION:
@app.route('/unprotected')
def unprotected():
    return 'This is unprotected area'

@app.route('/protected')
def protected():
    return 'This is protected area'

@app.route('/login')
def login():
    return 'You are now logged in'

# start the server
if __name__ == '__main__':
    app.run(debug=True)
