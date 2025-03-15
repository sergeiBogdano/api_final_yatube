from rest_framework import permissions, status, viewsets, filters
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post


from .permissions import IsAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAuthorOrReadOnly
    ]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["following__username"]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        following_user = serializer.validated_data["following"]

        if following_user == user:
            raise ValidationError(
                {"detail": "Нельзя подписаться на самого себя."}
            )

        if Follow.objects.filter(user=user, following=following_user).exists():
            raise ValidationError(
                {"detail": "Вы уже подписаны на этого пользователя."}
            )

        serializer.save(user=user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        post = Post.objects.get(id=post_id)
        serializer.save(author=self.request.user, post=post)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(
                "У вас нет прав на удаление этого комментария."
            )
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self):
        return Response(
            {
                'detail': 'Создание групп доступно только через админ-панель.'
            },
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
