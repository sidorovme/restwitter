from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id', 'author', 'created_at', 'updated_at', 'text']
