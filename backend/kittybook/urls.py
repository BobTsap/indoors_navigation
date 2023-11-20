from kitty.views import KittyViewSet
from message.views import ChatMessagesView
from message import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions, routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'cats', KittyViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/conversations/start/', views.start_convo, name='start_convo'),
    path('api/conversations/<int:convo_id>/', views.get_conversation, name='get_conversation'),
    path('api/conversations/', views.conversations, name='conversations'),
    path('api/messages/create/', views.CreateMessageView.as_view(), name='create_message'),
    path('api/<int:chat_id>/messages/', ChatMessagesView.as_view(), name='chat-messages'),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')), 
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
