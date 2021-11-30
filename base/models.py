from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4, 
                            editable=False, 
                            unique=True)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4, 
                            editable=False, 
                            unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4, 
                            editable=False, 
                            unique=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, 
                                    related_name='members', 
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at', '-updated_at']
        
    def __str__(self):
        return self.name


class Message(models.Model):
    id = models.UUIDField(primary_key=True, 
                            default=uuid.uuid4, 
                            editable=False, 
                            unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-updated_at']

    def __str__(self):
        return self.body[0:50]