from django.shortcuts import render
from rest_framework import generics, status
from .serializers import SignupSerializer
from rest_framework.response import Response

# Create your views here.

class SignupView(generics.GenericAPIView):
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)