from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from django.conf import settings

from . import googlehelper
from .register import register_social_user


# serializer for google social auth
class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        print("******************************* inside validate_auth_token *******************************")
        user_data = googlehelper.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or has expired.Please log in again.'
            )
        
        # checking the client id to be same as the one in the settings (after setting GOOGLE_CLIENT_ID in settings.py from .env file)
        # if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
        #     raise AuthenticationFailed('not valid google authentication')

        # user_id = user_data['sub']
        email = user_data['email']
        # name = user_data['name']
        auth_provider = 'google'

        return register_social_user(auth_provider=auth_provider, email=email)