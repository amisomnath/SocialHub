from django.db.models import Q
from rest_framework import status, generics, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from users.models import CustomUser
from .models import Post, Tag
from .serializers import PostSerializer, PostDetailSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class CustomUserRateThrottle(UserRateThrottle):
    rate = '10/minute'


class PostAPIView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomUserRateThrottle]

    def filter_by_author(self, author_id):
        queryset = self.get_queryset().filter(author=author_id)
        return queryset

    def get(self, request, *args, **kwargs):
        author_id = request.query_params.get('author_id')
        title = request.query_params.get('title')
        body = request.query_params.get('body')
        author = request.query_params.get('author')
        search_query = request.query_params.get('search')
        if request.user.is_superuser:
            queryset = Post.objects.all()
        else:
            queryset = Post.objects.filter(author=request.user)
        if author_id:
            try:
                author = CustomUser.objects.get(pk=author_id)
                queryset = self.filter_by_author(author)
                page = self.paginate_queryset(queryset)
                serializer = PostSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            except CustomUser.DoesNotExist:
                return Response({"error": "Author not found."}, status=status.HTTP_404_NOT_FOUND)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__username__icontains=search_query)
            )

        if title:
            queryset = queryset.filter(title__icontains=title)

        if body:
            queryset = queryset.filter(body__icontains=body)

        if author:
            queryset = queryset.filter(author__username=author)

        if kwargs.get('pk'):
            post = generics.get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
            if post.author == request.user or request.user.is_superuser:
                serializer = PostDetailSerializer(post)
                return Response(serializer.data)
            else:
                raise PermissionDenied("You don't have permission to view this post.")

        page = self.paginate_queryset(queryset)
        serializer = PostSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['author'] = request.user.id
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        post = generics.get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        if post.author == request.user or request.user.is_superuser:
            serializer = self.get_serializer(post, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise PermissionDenied("You don't have permission to edit this post.")

    def delete(self, request, *args, **kwargs):
        post = generics.get_object_or_404(self.get_queryset(), pk=kwargs['pk'])
        if post.author == request.user or request.user.is_superuser:
            post.is_deleted = True
            post.save()
            return Response({'message': 'Post deleted'}, status=status.HTTP_204_NO_CONTENT)
        else:
            raise PermissionDenied("You don't have permission to delete this post.")