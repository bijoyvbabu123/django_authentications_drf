from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    @staticmethod
    def validate(auth_token):
        print(auth_token)
        print("******************************* inside validate *******************************")
        try:
            print("******************************* inside validate  try block *******************************")

            # idinfo = id_token.verify_oauth2_token(auth_token, requests.Request()) # this is for OAuth 2.0 authorization server
            # idinfo = id_token.verify_firebase_token(auth_token, requests.Request()) # this is for Firebase
            # try adding client_id as the third parameter in the verify_token function
            idinfo = id_token.verify_token(auth_token, requests.Request())
            print("******************************* inside validate try, after verify *******************************")
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
            
        except:
            return "The token is invalid or has expired."