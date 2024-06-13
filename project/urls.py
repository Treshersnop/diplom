from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat.urls', namespace='chat')),
    path('', include('core.urls', namespace='core')),
    path('', include('training_course.urls', namespace='course')),
    path('webpush/', include('webpush.urls')),
    ]
