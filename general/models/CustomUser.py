
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from cloudinary.models import CloudinaryField

class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    birthday = models.DateField()
    gender = models.CharField(max_length=10)
    looking_for = models.CharField(max_length=10)
    marital_status = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    email_verified = models.BooleanField(default=False)
    
    # New fields
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    birthplace = models.CharField(max_length=100, blank=True, null=True)
    fav_tv_shows = models.TextField(blank=True, null=True)
    fav_music_bands = models.TextField(blank=True, null=True)
    fav_movies = models.TextField(blank=True, null=True)
    fav_games = models.TextField(blank=True, null=True)
    cover_photo = CloudinaryField('cover_photo', blank=True, null=True)

    # friends = models.ManyToManyField('self', blank=True, symmetrical=True)
    friends = models.ManyToManyField("self", blank=True)

    
    # Make email unique
    email = models.EmailField(unique=True)

    # Override the groups and user_permissions fields with unique related names
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.username
