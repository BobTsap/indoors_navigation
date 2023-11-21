from django.shortcuts import get_object_or_404
from message.models import Chat, Message
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChatListSerializer, ChatSerializer, MessageSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def start_convo(request, ):
    """
    Start a new conversation with a user.

    Returns:
    - If the conversation is successfully started, redirect to the conversation page.
    - If the user does not exist, return a response with an error message.
    """
    data = request.data
    username = data.pop('username')
    try:
        participant = User.objects.get(username=username)
        print(participant)
    except User.DoesNotExist:
        return Response(
            {'message': 'Пользователя с таким именем не существует'}
        )
    conversation = Chat.objects.filter(
        Q(from_user=request.user, to_user=participant) |
        Q(from_user=participant, to_user=request.user)
    )
    if conversation.exists():
        return redirect(
            reverse('get_conversation', args=(conversation[0].id,))
        )
    else:
        conversation = Chat.objects.create(
            from_user=request.user, to_user=participant)
        return Response(ChatSerializer(instance=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    """
    Retrieve a conversation by its ID.
    Returns:
    - If the conversation exists and the user has access to it, return the conversation data.
    - If the conversation does not exist or the user does not have access, return an error message.
    """
    conversation = get_object_or_404(Chat, id=convo_id)
    if (
        request.user != conversation.from_user 
        and request.user != conversation.to_user
        ):
        return Response({'message': 'У вас нет доступа к этому чату.'})
    serializer = ChatSerializer(instance=conversation)
    return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    """
    Retrieve a list of conversations for the current user.
    Returns:
    - The list of conversations for the current user.
    """
    conversation_list = get_object_or_404(Chat, Q(from_user=request.user) |
                                            Q(to_user=request.user))
    serializer = ChatListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)


class CreateMessageView(APIView):
    """
    Create a new message in a chat room.

    This API view expects the following data in the request body:
    - chat_room
    - text
    """
    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ChatMessagesView(ListAPIView):
    """
    Retrieve a list of messages in a chat room.
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        chat_id = self.kwargs['chat_id']
        return get_object_or_404(Message, chat_room_id=chat_id)
