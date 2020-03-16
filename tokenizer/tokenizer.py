import jwt
import datetime

class Tokenizer:
    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    def createToken(self, username, secretKey):
        # define content as a mix of username and expiration date
        tokenExpiry = setupExpiry()
        tokenContent = {
            'user': username,
            'expiration': tokenExpiry
        }

        # 'crypt' it this way:
        fullToken = jwt.encode(tokenContent, secretKey, algorithm='HS256')
        return fullToken

    # returns a decoded token
    def decodeToken(self, rawData, secretKey):
        output = jwt.decode(rawData, secretKey)
        print("Decoded token: " + output)
        return output


    # 👇 DIFFERENT STRATEGIES POSSIBLE 👇
    def setupExpiry():
        # sets token expiration to 30 minutes from now
        return str(datetime.datetime.utcnow() + datetime.timedelta(minutes=30))
