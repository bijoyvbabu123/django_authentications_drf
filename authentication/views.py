from django.shortcuts import render
from rest_framework import generics, status
from .serializers import SignupSerializer
from .models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.permissions import IsAuthenticated

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

        # current_user = User.objects.get(email=serializer.data['email'])
        # refresh_token = RefreshToken.for_user(current_user) # Create a refresh token for the user
        # refresh_token.access_token gives the access token associated with the refresh token

        # passing the request to TokenObtainPairView to get the refresh and access token
        response = TokenObtainPairView.as_view()(request._request)  # request._request is the original request in django.request object
        print(type(response.data['refresh']), "refresh token : ", response.data['refresh'])   # gives the refresh token
        print(type(response.data['access']),"access token : ", response.data['access'])    # gives the access token



        return Response(serializer.data, status=status.HTTP_201_CREATED)


# a simple view to test the authentication. For this view, we need to pass the access token in the authorization header (bearer token)
class TestView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user.email
        msg = f'Hello, {user}'
        return Response({'message': msg})