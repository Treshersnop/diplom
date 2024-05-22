from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title='LessonPark',
        default_version='v1',
        description='LessonPark',
    ),
    permission_classes=[permissions.IsAdminUser],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls', namespace='chat')),
    path('', include('core.urls', namespace='core')),
    path('', include('training_course.urls', namespace='course')),
    path('backend/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
