# Simple JWT authentication template
This repository represents the source code template for `JWT` based authentication.
It can be used as starting point for more complex projects and needs.

## Installation and usage
Perhaps the easiest way to start using this template would be as follows:
  - `clone` this repository
  - `cd flask-auth-template`
  - `pip install requirements.txt`

**NOTE:** if you're on `MacOS` platforms, there might be a struggle with running this project due to known collision of `Python2.7` and `Python3+`. By default `pip` will (assume) install dependencies to Python2 while `pip3` will place them under Python3.
If you're having trouble starting this project, try installing all the requirements using: `pip3 install requirements.txt`

### JWT based
`JSON Web Tokens` - or [JWT](https://jwt.io/) in short - are the foundation of the authentication mechanism presented here.  
Be sure **not to forget** to decode/encode token generation at your own strategy. Follow code comments for exact place where you need to modify or customise this behaviour.

### No database !
Any DB layer has been **intentionally** omitted to allow space for your own implementation. In this form, the code template stores all generated tokens **in memory** and are only valid until next server restart. For more convenient mechanism, store your `tokens` in some form of persistent storage.

#### Word of wisdom
If you ever get stuck during coding, remember that `sudo` is your friend. If that doesn't help, just one cold 🍺 can magically make your life look way more beautiful.

----

Copyright © 2020 Veljko Tekelerović
