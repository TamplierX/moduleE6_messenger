from rest_framework import serializers
from .models import Chat, Message


class ChatSerializer(serializers.ModelSerializer):
    is_admin = serializers.ReadOnlyField(source='is_admin.username')
    messages = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'is_admin', 'is_group', 'members', 'messages']


class MessageSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Message
        fields = ['id', 'chat', 'author', 'text', 'created']

    def validate(self, data):
        if not data.get('chat'):
            raise serializers.ValidationError("Chat ID is required.")
        if not data.get('text'):
            raise serializers.ValidationError("Message text is required.")
        return data
