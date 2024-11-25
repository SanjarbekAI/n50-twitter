from rest_framework import serializers

from accounts.serializers import UserSerializer
from tweets.models import TweetModel, CommentModel


class TweetSerializer(serializers.ModelSerializer):
    child_count = serializers.SerializerMethodField()

    class Meta:
        model = TweetModel
        fields = ['id', 'text', 'image', 'created_at', 'parent', 'child_count']
        extra_kwargs = {
            'image': {'required': False},
            'user': {'required': False},
            'parent': {'required': False},
        }

    def get_child_count(self, obj):
        return obj.children.count()


class TweetCommentSerializer(serializers.ModelSerializer):
    child_count = serializers.SerializerMethodField(method_name='get_child_count')
    user = UserSerializer(read_only=True)
    tweet = serializers.PrimaryKeyRelatedField(queryset=TweetModel.objects.all())

    class Meta:
        model = CommentModel
        fields = ['id', 'comment', 'user', 'created_at', 'parent', 'tweet', 'child_count']
        extra_kwargs = {
            'parent': {'required': False},
        }

    @staticmethod
    def get_child_count(obj):
        return obj.children.count()
