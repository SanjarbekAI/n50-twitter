from django.contrib.auth.models import AbstractUser
from django.db import models


class UserModel(AbstractUser):
    email = models.EmailField(null=False, blank=False, unique=True)


class VerificationModel(models.Model):
    user = models.OneToOneField(UserModel,
                                on_delete=models.CASCADE,
                                related_name='verification_codes')
    code = models.CharField(max_length=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.code}"

    class Meta:
        verbose_name = "Verification code"
        verbose_name_plural = "Verification codes"
        unique_together = ('user', 'code',)


class FollowerModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='following')
    to_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} following to {self.to_user.email}"

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        unique_together = ['user', 'to_user']
