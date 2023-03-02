from django.contrib.auth import authenticate
from django.conf import settings

from rest_framework.exceptions import AuthenticationFailed

from authentication.models import User

def register_social_user(auth_provider, email):
    filter_user_email = User.objects.filter(email=email)

    if filter_user_email.exists():

        if filter_user_email[0].auth_provider == auth_provider:

            registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)

            return {
                'email': registered_user.email,
                'token': registered_user.tokens()
            }
        
        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filter_user_email[0].auth_provider
            )
    
    else:

        u = {
            'email': email,
            'password': settings.SOCIAL_SECRET,
        }
        user = User.objects.create_user(**u)
        user.is_verified = True
        user.auth_provider = auth_provider
        user.save()

        new_registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)

        return {
            'email': new_registered_user.email,
            'token': new_registered_user.tokens()
        }