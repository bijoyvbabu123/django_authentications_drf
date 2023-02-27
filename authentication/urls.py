from django.urls import path
from .views import SignupView, TestView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('testauth/', TestView.as_view(), name='testauth'),
    path('loginjwt/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # this is actually the login view, it returns the refresh and access token
    path('jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]