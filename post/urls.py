from django.urls import re_path, path
from rest_framework.routers import DefaultRouter
from post.views import PostAPIView, TagViewSet

router = DefaultRouter()
router.register('tag', TagViewSet, basename='tag')

urlpatterns = [

    # Retrieve, update, or delete a specific post by ID
    path('<int:pk>/', PostAPIView.as_view(), name='post-detail'),

    # List all posts and create a new post
    path('', PostAPIView.as_view(), name='post-list-create'),
]

urlpatterns = urlpatterns + router.urls
