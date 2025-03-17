from django.contrib.auth import get_user_model

from posts.models import Comment, Follow, Group, Post

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'text', 'created')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, value):
        request = self.context.get('request')
        if request is None:
            return value
        if request.user == value:
            raise serializers.ValidationError(
                "Нельзя подписаться на самого себя."
            )
        return value

    def validate(self, data):
        user = self.context['request'].user
        following = data['following']

        if Follow.objects.filter(user=user, following=following).exists():
            raise serializers.ValidationError(
                "Вы уже подписаны на этого пользователя."
            )

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
