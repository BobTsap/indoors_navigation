from django.contrib import admin
from .models import Kitty

@admin.register(Kitty)
class KittyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birth_year', 'color', 'breed', 'owner')
    list_filter = ('color', 'breed', 'owner__username')
    search_fields = ('name', 'color', 'breed', 'owner__username')
    empty_value_display = '-пусто-'
