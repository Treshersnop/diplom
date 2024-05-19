from django.urls import path

from training_course import views

app_name = 'training_course'

urlpatterns = [
    path('course/list/', views.CourseList.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
    path('course/create/', views.CourseCreate.as_view(), name='course_create'),

    path('subscription/<int:pk>/create/', views.create_subscription, name='create_subscription'),
    path('subscription/<int:pk>/delete/', views.delete_subscription, name='delete_subscription')
]
