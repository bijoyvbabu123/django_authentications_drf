from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import GoogleSocialAuthSerializer


# Create your views here.

# class for google authentication
class GoogleSocialAuthView(generics.GenericAPIView):
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)