from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Kitty
from .serializers import KittySerializer


class KittyViewSet(viewsets.ModelViewSet):
    '''
    API endpoint for managing Kitties.
    '''
    queryset = Kitty.objects.all()
    serializer_class = KittySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        '''
        The queryset of Kitties owned by the current user.
        '''
        queryset = get_object_or_404(Kitty, owner=self.request.user)
        return queryset
    
    def get_object(self):
        '''
        Returns а Kitty object with the required id.
        '''
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
    
    def perform_create(self, serializer):
        '''
        Saves a new Kitty object with the current user as the owner.
        '''
        serializer.save(owner=self.request.user)
