from rest_framework import serializers

from message.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ('chat_room',)


class ChatListSerializer(serializers.ModelSerializer):
    # last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id','from_user', 'to_user']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from_user'] = instance.from_user.username
        representation['to_user'] = instance.to_user.username
        return representation

    # def get_last_message(self, instance):
    #     message = instance.message_set.first()
    #     return MessageSerializer(instance=message).data


class ChatSerializer(serializers.ModelSerializer):

    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['to_user', 'message_set']
