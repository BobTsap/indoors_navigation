import datetime as dt
from django.core.validators import MaxValueValidator, MinValueValidator

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Kitty(models.Model):
    '''
    A model that collect information about cats.
    '''
    name = models.CharField(
        max_length=100,
        verbose_name='Имя котика',
    )
    birth_year = models.IntegerField(
        verbose_name='Дата рождения',
        validators=[MinValueValidator(
            1985, message=f'Врятли котики столько живут,'
                        f'если это правда - то обратитесь в книгу рекордов Гиннеса!'
        ), MaxValueValidator(
            dt.datetime.now().year, message=f'Возраст не может быть меньше 0'
        )]
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
