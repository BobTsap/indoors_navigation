from rest_framework import serializers

from message.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('chat_room',)


class ChatListSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['from_user', 'to_user', 'last_message']

    def get_last_message(self, instance):
        message = instance.message_set.first()
        return MessageSerializer(instance=message).data


class ChatSerializer(serializers.ModelSerializer):

    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['from_user', 'to_user', 'message_set']
