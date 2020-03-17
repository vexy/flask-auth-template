# -*- coding: utf-8 -*-
import jwt
import datetime

class Tokenizer():
    def __init__(self, key):
        self.secretKey = key

    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    def createToken(self, username):
        # define content as a mix of username and expiration date
        tokenExpiry = self.setupExpiry()
        tokenContent = {
            'user': username,
            'expiration': tokenExpiry
        }

        # 'crypt' it this way:
        fullToken = jwt.encode(tokenContent, self.secretKey, algorithm='HS256')
        return fullToken

    # returns a decoded token
    def decodeToken(self, rawToken):
        output = jwt.decode(rawToken, self.secretKey, algorithms=['HS256'])
        return output


    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    def setupExpiry(self):
        # sets token expiration to 30 minutes from now
        return str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
