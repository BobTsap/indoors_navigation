from django.db import models

from kitty.models import User


class Chat(models.Model):
    from_user = models.ForeignKey(
        User,
        verbose_name='Отправитель',
        related_name='chats_sent',
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        User,
        verbose_name='Получатель',
        related_name='chats_received',
        on_delete=models.CASCADE
    )

    pass

class Message(models.Model):
    text = models.TextField(
        verbose_name='Текст сообщения',
    )
    sender = models.ForeignKey(
        User,
        verbose_name='Отправитель',
        on_delete=models.CASCADE,
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
        ordering=['pub_date']
 
    def __str__(self):
        return self.text
