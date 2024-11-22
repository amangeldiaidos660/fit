from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    chat_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.email
