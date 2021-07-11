from rest_framework import serializers

from core.models import Post, UserFollowing


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post object"""

    class Meta:
        model = Post
        fields = ('id', 'description', 'created_at')
        read_only_fields = ('id', 'created_at',)


class FollowersSerializer(serializers.ModelSerializer):
    """Serialize followers"""
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ('following_user_id', 'created_at', 'email')

    def get_email(self, obj):
        return obj.following_user_id.email


class FollowingSerializer(serializers.ModelSerializer):
    """Serialize following"""
    email = serializers.SerializerMethodField()

    class Meta:
        model = UserFollowing
        fields = ('user_id', 'created_at', 'email')

    def get_email(self, obj):
        return obj.user_id.email


class TimelineSerializer(serializers.ModelSerializer):
    """Serialize timeline posts"""
    email = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('description', 'email', 'created_at')

    def get_email(self, obj):
        return obj.user.email
