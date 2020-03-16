# Authentication gate with Flask & JWT
This repository represents the source code template for micro webserver that provides authentication gate for your protected resources.

It is written in `Python` using `Flask` framework. `JWT` tokens are base authentication mechanism.  
Some of the provided strategies are to basic/simple for **serious**, production level webserver. Use this template as starting point for more complex projects and requirements.

### JWT based
`JSON Web Tokens` - or [JWT](https://jwt.io/) in short - is the foundation authentication principle used in this template.  
Be sure **not to forget** to encode/decode token generation at your own strategy. Follow code comments for exact place where you could modify or customise this behaviour.

### No database !
DB layer has been **intentionally omitted** to allow space for your own implementation. In present form, the code handles all tokens **in memory**, making the tokens  available only while the server is running. All tokens will disappear after the server shuts down.  
For more convenient mechanism, store your `tokens` in some form of persistent storage, or reuse them in different way.

### Installation
Before you begin:
```
git clone
cd flask-auth-template
```
Then choose between automatic or manual dependency installation:

- installing via pre-packed script (_automatic_)
```
# On UNIX based platforms, just:
$ . install-dependencies.sh
```
- manual dependency installation
```
# make sure pip3 is installed
pip3 install -r requirements.txt
```

### Starting server
Template will setup and start a server listening on `localhost`. Check the debug output for more information.  

To start the server:
```
python3 auth-module.py
```
or run the start script
```
$ . start.sh  #
```

**:NOTE:** for `MacOS` users:  
There might be a struggle with starting this project, due to known collision of `Python2.xx` and `Python3.xx` coexisting on same platform. The conflict might be manifested as good ol' *"Module Import Error"* no matter which Python you are using.
To solve this, you might have to "fix" (play around with) your `PYTHONPATH`.  Check out this [article](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html) for more information.

----

#### Word of wisdom
If you ever get stuck remember that `sudo` is your friend. If it doesn't help, start thinking how one cold 🍺 can magically improve your understanding of the 🌎.


Copyright © 2020 Veljko Tekelerović  
MIT License
