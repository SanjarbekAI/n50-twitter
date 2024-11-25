from django.db import models

from accounts.models import UserModel


class TweetModel(models.Model):
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               related_name='children',
                               null=True, blank=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='tweets')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='tweets/', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "tweet"
        verbose_name_plural = "tweets"


class CommentModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comments')
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='children'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class PostLikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='likes')
    tweet = models.ForeignKey(TweetModel, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.id} to {self.tweet.id}"

    class Meta:
        verbose_name = "post like"
        verbose_name_plural = "post likes"
        unique_together = ('user', 'tweet')


class CommentLikeModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(CommentModel, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.id} to {self.comment.comment}"

    class Meta:
        verbose_name = "comment like"
        verbose_name_plural = "comment likes"
        unique_together = ('user', 'comment')
