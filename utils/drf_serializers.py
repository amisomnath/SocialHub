from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CustomRegisterSerializer(RegisterSerializer):
    is_agreed = serializers.BooleanField(required=True)

    registration_request = None

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'is_agreed': self.validated_data.get('is_agreed', False),
        }

    def validate(self, data):
        data = super().validate(data)

        is_agreed = data.get('is_agreed')
        if not is_agreed:
            raise serializers.ValidationError('is_agreed - this field is required.')

        return data

    def save(self, request):
        user = super().save(request)
        user.is_agreed = self.cleaned_data['is_agreed']
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'age', 'gender', 'is_account_active')


class BaseStatusResponseSerializer(serializers.Serializer):
    STATUS_OK = 'ok'
    STATUS_ERROR = 'error'
    STATUS_CHOICE = (
        (STATUS_OK, 'ok'),
        (STATUS_ERROR, 'error'),
    )

    status = serializers.ChoiceField(choices=STATUS_CHOICE)
