from better_profanity import profanity

from rest_framework import serializers

from message.models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    def validate_text(self, value):
        """
        Filters profanity from the message text.
        Return *** instead of abusive text.
        """
        value = profanity.censor(value)
        return value
    
    def to_representation(self, instance):
        '''
        Customize the representation of a Chat instance.
        Return username instead id.
        '''
        representation = super().to_representation(instance)
        representation['sender'] = instance.sender.username
        return representation
    
    class Meta:
        model = Message
        fields = ['id', 'text', 'pub_date', 'sender', 'chat_room']


class ChatListSerializer(serializers.ModelSerializer):
    '''
    Serializer for the list of Chat instances.
    '''
    class Meta:
        model = Chat
        fields = ['id', 'to_user']

    def to_representation(self, instance):
        '''
        Customize the representation of a Chat instance.
        Return username instead id.
        '''
        representation = super().to_representation(instance)
        representation['to_user'] = instance.to_user.username
        return representation


class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for the Chat model.
    """
    message_set = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['to_user', 'message_set']
