from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Kitty, User
from .serializers import KittySerializer


class KittyViewSet(viewsets.ModelViewSet):
    queryset = Kitty.objects.all()
    serializer_class = KittySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Kitty.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
