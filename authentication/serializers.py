from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, max_length=128, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        # if not User.objects.filter(email=email).exists():
        #     raise serializers.ValidationError({'email': ('User with given email does not exists')})
        return attrs

        # return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


# serializer for email verification
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']