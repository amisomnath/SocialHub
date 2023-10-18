from rest_framework import serializers
from .models import Post, Tag
from users.serializers import UserShortSerializers


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'tags', 'author')

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'])
            post.tags.add(tag)

        return post


class PostDetailSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'tags', 'author')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.author:
            response['author'] = UserShortSerializers(instance.author).data
        return response

    # Add the "body" field to the serializer
    extra_kwargs = {
        'body': {'required': True}
    }
