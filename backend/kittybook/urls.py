from kitty.views import KittyViewSet
from message import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'cats', KittyViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/conversations/start/', views.start_convo, name='start_convo'),
    path('api/conversations/<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('conversations/', views.conversations, name='conversations'),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
