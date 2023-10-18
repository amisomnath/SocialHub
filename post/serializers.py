from rest_framework import serializers
from .models import Post, Tag
from users.serializers import UserShortSerializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'tags', 'author')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.tags:
            response['tags'] = TagSerializer(instance.tags).data
        return response


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'tags', 'author')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.tags:
            response['tags'] = TagSerializer(instance.tags).data
        if instance.author:
            response['author'] = UserShortSerializers(instance.author).data
        return response

