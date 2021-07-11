from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Post, UserFollowing

from socialnetwork import serializers


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin):
    """Manage posts in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user) \
            .order_by('-created_at')

    def perform_create(self, serializer):
        """Create a new Post"""
        serializer.save(user=self.request.user)


class UserFollowingViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin):
    """manage user following"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserFollowing.objects.all()
    serializer_class = serializers.FollowersSerializer

    def get_queryset(self):
        """Return user following"""
        return self.queryset.filter(user_id=self.request.user) \
            .order_by('-created_at')

    def perform_create(self, serializer):
        """Create following list"""
        serializer.save(user_id=self.request.user)


class UserFollowerViewSet(viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    """List user followers"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = UserFollowing.objects.all()
    serializer_class = serializers.FollowingSerializer

    def get_queryset(self):
        """Returns followers list"""
        return self.queryset.filter(following_user_id=self.request.user) \
            .order_by('-created_at')


class TimelineViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    """Show posts"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = serializers.TimelineSerializer

    def get_queryset(self):
        userList = UserFollowing.objects.filter(user_id=self.request.user) \
            .values_list('following_user_id', flat=True)
        return self.queryset.filter(user__in=userList) \
            .order_by('-created_at')[:10]
