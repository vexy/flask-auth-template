# Authentication mechanism based on Flask + JWT
This repository represents the source code template for `Flask` implementation of `JWT` based authentication.
It can be used as starting point for more complex projects and requirements or can be completely customised to serve your needs.

## Installation and usage
Perhaps the easiest way to start would be executing `startup.sh` script. Simple `(user)$ . startup.sh` would do the trick on UNIX based systems.

Alternatively, step by step guide would be:
  - `clone` this repository (*aim for master*)
  - `cd flask-auth-template`
  - `pip3 install -r requirements.txt`
  - `python3 auth-module.py`

**NOTE:** if you're on `MacOS` platforms, there might be a struggle with running this project due to known collision of `Python2.7` and `Python3+`. The conflict might be seen as "Module Import Error" no matter which Python you are using.
To solve this, you might have to "fix" your `PYTHONPATH`.  Check out this [article](https://bic-berkeley.github.io/psych-214-fall-2016/using_pythonpath.html) for more information.

### JWT based
`JSON Web Tokens` - or [JWT](https://jwt.io/) in short - are the foundation of the authentication mechanism presented here.  
Be sure **not to forget** to decode/encode token generation at your own strategy. Follow code comments for exact place where you need to modify or customise this behaviour.

### No database !
Any DB layer has been **intentionally** omitted to allow space for your own implementation. In this form, the code template stores all generated tokens **in memory** and are only valid until next server restart. For more convenient mechanism, store your `tokens` in some form of persistent storage.

#### Word of wisdom
If you ever get stuck during coding, remember that `sudo` is your friend. If that doesn't help, just one cold 🍺 can magically make your life look way more beautiful.

----

Copyright © 2020 Veljko Tekelerović
