from django.shortcuts import render
from message.models import Chat
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import ChatListSerializer, ChatSerializer
from django.db.models import Q
from django.shortcuts import redirect, reverse


@api_view(['POST'])
def start_convo(request, ):
    data = request.data
    username = data.pop('username')
    try:
        participant = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'message': 'You cannot chat with a non existent user'})

    conversation = Chat.objects.filter(Q(from_user=request.user, to_user=participant) |
                                               Q(from_user=participant, to_user=request.user))
    if conversation.exists():
        return redirect(reverse('get_conversation', args=(conversation[0].id,)))
    else:
        conversation = Chat.objects.create(inifrom_usertiator=request.user, to_user=participant)
        return Response(ChatSerializer(instance=conversation).data)


@api_view(['GET'])
def get_conversation(request, convo_id):
    conversation = Chat.objects.filter(id=convo_id)
    if not conversation.exists():
        return Response({'message': 'Chat does not exist'})
    else:
        serializer = ChatSerializer(instance=conversation[0])
        return Response(serializer.data)


@api_view(['GET'])
def conversations(request):
    conversation_list = Chat.objects.filter(Q(from_user=request.user) |
                                                    Q(to_user=request.user))
    serializer = ChatListSerializer(instance=conversation_list, many=True)
    return Response(serializer.data)
