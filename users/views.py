from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from django.template.loader import render_to_string
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from yaml import serialize
from users.models import CustomUser
from users.serializers import UserSerializer


class UserViewSet(generics.UpdateAPIView, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    http_method_names = ('get', 'put', )
    queryset = CustomUser.objects.all()

    def get_object(self):
        obj = get_object_or_404(self.queryset, pk=self.request.user.pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        result = super().update(request, *args, **kwargs)

        if 'username' in request.data:
            user = self.get_object()
            refresh = RefreshToken.for_user(user)
            result.data['refresh_token'] = str(refresh)
            result.data['access_token'] = str(refresh.access_token)

        return result

class CustomRegisterView(RegisterView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_name = 'Friend'
        if response.data['user']['first_name'] is not None:
            user_name = response.data['user']['first_name']
        return response
