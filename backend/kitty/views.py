from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Kitty
from .serializers import KittySerializer


class KittyViewSet(viewsets.ModelViewSet):
    queryset = Kitty.objects.all()
    serializer_class = KittySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = get_object_or_404(Kitty, owner=self.request.user)
        return queryset

        # return Kitty.objects.filter(owner=self.request.user)
    
    def get_object(self):
            queryset = self.get_queryset()
            obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
            return obj
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
