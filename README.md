# Authentication mechanism: Flask + JWT
This repository represents the source code template for `Flask` implementation of `JWT` based authentication.
It can be used as starting point for more complex projects and requirements or can be completely customised to serve your needs.

## Installation and usage
Perhaps the easiest way to start would be executing `startup.sh` script. Simple `(user)$ . startup.sh` would do the trick on UNIX based systems.

Alternatively, step by step guide would be:
  - `clone` this repository (*aim for master*)
  - `cd flask-auth-template`
  - `pip3 install -r requirements.txt`
  - `python3 auth-module.py`

**:NOTE:**  
If you're on `MacOS` platforms, there might be a struggle with starting this project, due to known collision of `Python2.xx` and `Python3.xx` coexisting on same platform. The conflict might be manifested as good ol' *"Module Import Error"* no matter which Python you are using.
To solve this, you might have to "fix" (play around with) your `PYTHONPATH`.  Check out this [article](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html) for more information.

### JWT based
`JSON Web Tokens` - or [JWT](https://jwt.io/) in short - is the foundation authentication principle used in this template.  
Be sure **not to forget** to encode/decode token generation at your own strategy. Follow code comments for exact place where you could modify or customise this behaviour.

### No database !
DB layer has been **intentionally omitted** to allow space for your own implementation. In present form, the code handles all tokens **in memory**, making the tokens  available only while the server is running. All tokens will disappear after the server shuts down.  
For more convenient mechanism, store your `tokens` in some form of persistent storage, or reuse them in different way.

#### Word of wisdom
If you ever get stuck remember that `sudo` is your friend. If it doesn't help, start thinking how one cold 🍺 can magically improve your understanding of the 🌎.

----

Copyright © 2020 Veljko Tekelerović
