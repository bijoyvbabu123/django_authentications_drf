from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.conf import settings

from .serializers import (
    SignupSerializer,
    EmailVerificationSerializer,
)
from .models import User
from .utils import (
    create_verification_email,
    EmailUtil,
    check_and_verify_user,
)

from rest_framework import generics, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import jwt

# Create your views here.

class SignupView(generics.GenericAPIView):
    """
    User Signup using email and password.
    """

    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # generating a token for the current user
        curr_user = User.objects.get(email=serializer.data['email'])
        a_token = str(RefreshToken().for_user(user=curr_user).access_token)

        # sending the verification email
        v_mail = create_verification_email(request=request, user=curr_user, token=a_token)
        EmailUtil.send_email(v_mail)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# view for email verification
class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer()

    def get(self, request):
        token = request.GET.get('token')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            check_and_verify_user(pkey=payload['user_id'])
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



# a simple view to test the authentication. For this view, we need to pass the access token in the authorization header (bearer token)
class TestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user.email
        msg = f'Hello, {user}'
        return Response({'message': msg})