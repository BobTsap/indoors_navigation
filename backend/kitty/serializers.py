import base64
import datetime as dt

from django.core.files.base import ContentFile
from rest_framework import serializers

from kitty.models import Kitty
# from message.models import Chat, Message



class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class KittySerializer(serializers.ModelSerializer):

    age = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)
    image_url = serializers.SerializerMethodField(
        'get_image_url',
        read_only=True,
    )

    class Meta:
        model = Kitty
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def create(self, validated_data):
        cat = Kitty.objects.create(**validated_data)
        return cat

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get(
            'birth_year', instance.birth_year
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance
