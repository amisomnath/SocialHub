from django.urls import re_path, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

router = DefaultRouter()

urlpatterns = [

    # Blocked User Functionality Endpoints
    path('blocked-users/', CustomUserViewSet.as_view({'get': 'get_blocked_users'}), name='blocked-users'),
    path('block-user/<int:user_id>/', CustomUserViewSet.as_view({'post': 'block_user'}), name='block-user'),
    path('unblock-user/<int:user_id>/', CustomUserViewSet.as_view({'delete': 'unblock_user'}), name='unblock-user'),
]

urlpatterns = urlpatterns + router.urls
