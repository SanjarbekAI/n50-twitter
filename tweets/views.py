from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from tweets.models import TweetModel, CommentModel
from tweets.paginations import TweetsPagination
from tweets.permissions import IsOwnerOrReadOnly
from tweets.serializers import TweetSerializer, TweetCommentSerializer


class TweetViewSet(viewsets.ModelViewSet):
    serializer_class = TweetSerializer
    queryset = TweetModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = TweetsPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return TweetModel.objects.filter(parent__isnull=True)


class TweetChildListAPIView(generics.ListAPIView):
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = TweetsPagination

    def get_queryset(self):
        parent = self.request.query_params.get('parent')
        if parent is None:
            return []
        return TweetModel.objects.filter(parent_id=parent)


class TweetCommentViewSet(generics.ListCreateAPIView):
    serializer_class = TweetCommentSerializer
    queryset = CommentModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
    pagination_class = TweetsPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CommentModel.objects.filter(parent__isnull=True)


class TweetCommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TweetCommentSerializer
    queryset = CommentModel.objects.all()
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]

