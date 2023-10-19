from dj_rest_auth.registration.views import RegisterView
from django.db import transaction
from rest_framework import generics, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import CustomUser, BlockedUser
from users.serializers import UserSerializer, BlockedUserSerializer
from rest_framework.decorators import action


class UserViewSet(generics.UpdateAPIView, generics.RetrieveAPIView):
    serializer_class = UserSerializer
    http_method_names = ('get', 'put',)
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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['GET'], url_path='blocked-users', url_name='blocked-users')
    def get_blocked_users(self, request):
        blocked_users = BlockedUser.objects.filter(blocker=request.user)
        serializer = BlockedUserSerializer(blocked_users, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], url_path='block-user/(?P<user_id>[0-9]+)', url_name='block-user')
    def block_user(self, request, user_id):
        try:
            user_to_block = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if user_to_block == request.user:
            return Response({"error": "You cannot block yourself."}, status=status.HTTP_400_BAD_REQUEST)

        BlockedUser.objects.get_or_create(blocker=request.user, blocked_user=user_to_block)
        return Response({"message": f"You have blocked {user_to_block.username}."}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['DELETE'], url_path='unblock-user/(?P<user_id>[0-9]+)', url_name='unblock-user')
    def unblock_user(self, request, user_id):
        try:
            user_to_unblock = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        blocked_user = BlockedUser.objects.filter(blocker=request.user, blocked_user=user_to_unblock).first()
        if blocked_user:
            blocked_user.delete()
            return Response({"message": f"You have unblocked {user_to_unblock.username}."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": f"{user_to_unblock.username} is not in your blocked users list."},
                            status=status.HTTP_400_BAD_REQUEST)
