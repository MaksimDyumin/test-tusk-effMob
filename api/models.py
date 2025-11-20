from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    user = models.ForeignKey('auth_api.User', on_delete=models.CASCADE, related_name='posts')