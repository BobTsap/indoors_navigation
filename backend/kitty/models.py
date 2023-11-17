from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Kitty(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Имя котика',
    )
    birth_year = models.IntegerField(
        verbose_name='Дата рождения'
    )
    color = models.CharField(
        max_length=16,
        verbose_name='Окрас',
    )
    breed = models.CharField(
        max_length=32,
        verbose_name='Порода',
    )
    owner = models.ForeignKey(
        User, related_name='cats',
        on_delete=models.CASCADE
    )
    history = models.TextField(
        verbose_name='История о котике',
    )

    image = models.ImageField(
        upload_to='cats/images/',
        null=True,
        default=None
    )

    def __str__(self):
        return self.name
