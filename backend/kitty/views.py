from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Kitty
from .serializers import KittySerializer, UserSerializer


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
        return Kitty.objects.filter(owner=self.request.user)
    
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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


