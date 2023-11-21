from django.db import models

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()


class Chat(models.Model):
    '''
    A model that contains information about existing chats.
    '''
    from_user = models.ForeignKey(
        User,
        verbose_name='Отправитель',
        related_name='chats_sent',
        on_delete=models.SET_NULL,
        null=True,
    )
    to_user = models.ForeignKey(
        User,
        verbose_name='Получатель',
        related_name='chats_received',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        unique_together = ['from_user', 'to_user']


class Message(models.Model):
    '''
    A model for storing information about chat messages.
    '''
    text = models.TextField(
        verbose_name='Текст сообщения',
    )
    sender = models.ForeignKey(
        User,
        verbose_name='Отправитель',
        on_delete=models.SET_NULL,
        null=True,
    )
    pub_date = models.DateTimeField(
        'Дата сообщения', auto_now_add=True, db_index=True
    )
    chat_room = models.ForeignKey(
        Chat,
        verbose_name='Чат',
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['pub_date']

    def __str__(self):
        return self.text
