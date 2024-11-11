from rest_framework import serializers

from tweets.models import TweetModel


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
