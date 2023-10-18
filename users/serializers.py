import django.contrib.auth.password_validation as validate_password
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.validators import ASCIIUsernameValidator
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST
from users.models import CustomUser, BlockedUser
from utils.drf_serializers import BaseStatusResponseSerializer


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False, validators=(ASCIIUsernameValidator(), ))

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_agreed', 'age', 'gender', 'is_account_active')

    def update(self, instance, validated_data):
        user_data = validated_data

        for attr, value in list(user_data.items()):
            setattr(instance, attr, value)

        if CustomUser.objects.filter(username=instance.username).exclude(id=instance.id).exists():
            raise ParseError(
                detail='Unfortunately, the profile is busy',
                code=HTTP_400_BAD_REQUEST
            )
        elif CustomUser.objects.filter(email=instance.email).exclude(id=instance.id).exists():
            raise ParseError(
                detail='This email has already exist',
                code=HTTP_400_BAD_REQUEST
            )
        instance.save()
        return instance


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class UserShortSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = '__all__'
