from rest_framework import serializers

from message.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'to_user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['to_user'] = instance.to_user.username
        return representation


class ChatSerializer(serializers.ModelSerializer):

    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['to_user', 'message_set']
