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



