from django.contrib.auth.views import logout_then_login
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from core import views

app_name = 'core'

urlpatterns = [
    path('', RedirectView.as_view(url='course/list')),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('register/profile/', views.CreateProfile.as_view(), name='register_profile'),

    path('profile/<int:pk>', views.ProfileDetail.as_view(), name='profile'),
    path('profile/update/<int:pk>', views.ProfileUpdate.as_view(), name='profile_update'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
