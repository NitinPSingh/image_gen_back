# chatapp/serializers.py
from rest_framework import serializers
from .models import ChatInteraction, Chat, ChatFile

class ChatFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatFile
        fields = '__all__'
        read_only_fields = ['user']

class ChatSerializer(serializers.ModelSerializer):
    files = ChatFileSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'chat_content', 'created_at', 'is_bot', 'chat_interaction', 'files']

class ChatInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInteraction
        fields = ['id', 'user', 'timestamp']