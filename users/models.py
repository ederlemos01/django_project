from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='photos/')
    following = models.ManyToManyField('self', symmetrical=False,
                                       related_name='followers',blank=True)