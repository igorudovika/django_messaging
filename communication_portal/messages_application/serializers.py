from rest_framework import serializers

from .models import Messages
from django.contrib.auth.models import User


class MessagesBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']