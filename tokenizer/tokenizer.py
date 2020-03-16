import jwt
import datetime

class Tokenizer():
    secretKey = ''

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
        print("<TOKENIZER> content is:" + tokenContent)

        # 'crypt' it this way:
        fullToken = jwt.encode(tokenContent, self.secretKey, algorithm='HS256')
        print("<TOKENIZER> Token is" + fullToken)
        return fullToken

    # returns a decoded token
    def decodeToken(self, rawData):
        output = jwt.decode(rawData, self.secretKey)
        print("<TOKENIZER> Decoded token: " + output)
        return output


    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    def setupExpiry(self):
        # sets token expiration to 30 minutes from now
        return str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
