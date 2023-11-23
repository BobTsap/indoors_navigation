import base64
import datetime as dt
from better_profanity import profanity

from django.core.files.base import ContentFile
from rest_framework import serializers

from kitty.models import Kitty


class Base64ImageField(serializers.ImageField):
    '''
    Converts image data in base64 format to ContentFile.
    '''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class KittySerializer(serializers.ModelSerializer):
    '''
    Serializer for Kitty model.
    '''
    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Kitty
        fields = [
            'name', 'age', 'color',
            'breed', 'owner', 'history',
            'birth_year',
            'image', 'image_url'
        ]

    def get_image_url(self, obj):
        '''
        Retrieves the URL of the image, if it exists.
        Return URL of the image, if it exists.
        Otherwise, None.
        '''
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj):
        '''
        Calculates the age of the cat based on the year of birth.
        Return the ae of the Kitty.
        '''
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        '''
        Creates a new cat based on validated data.
        Return new Kitty object.
        '''

        # validated_data['birth_year'] = dt.datetime.now().year - int(validated_data.get('age'))
        cat = Kitty.objects.create(**validated_data)
        return cat
        # birth_year = validated_data.pop('birth_year')
        # kitty = Kitty.objects.create(
        #     birth_year=birth_year,  # Устанавливаем год рождения котика
        #     **validated_data  # Остальные данные
        # )
        # return kitty
        # cat = Kitty.objects.create(**validated_data)
        # return cat

    def update(self, instance, validated_data):
        '''
        Updates the data of an existing cat based on validated data.
        Return updated Kitty object.
        '''
        if instance.owner != self.context['request'].user:
            raise serializers.ValidationError(
                'Вы не являетесь владельцем этого котика')
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get(
            'birth_year', instance.birth_year
        )
        instance.image = validated_data.get('image', instance.image)
        if not instance.name:
            raise serializers.ValidationError("Имя отсутствует")
        if not instance.color:
            raise serializers.ValidationError("Отсутствует окрас")
        if not instance.birth_year:
            raise serializers.ValidationError("Не указан год рождения")
        if not instance.image:
            raise serializers.ValidationError("Без фотографии не интересно")
        instance.save()
        return instance

    def validate_history(self, value):
        '''
        Filters profanity in the history of the cat.
        '''
        value = profanity.censor(value)
        return value
