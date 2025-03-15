from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'author': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'text', 'created']
        read_only_fields = ['author', 'post']


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(read_only=True, slug_field='username')
    following = SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        request = self.context.get('request')
        if request is None:
            return data

        current_user = request.user
        following = data.get('following')

        if not following:
            raise serializers.ValidationError(
                "Поле 'following' обязательно."
            )

        if current_user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.'
            )

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError('Ошибка контекста запроса.')

        validated_data['user'] = request.user
        return super().create(validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
