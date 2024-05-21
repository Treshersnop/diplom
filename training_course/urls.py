from django.urls import path

from training_course import views

app_name = 'training_course'

urlpatterns = [
    path('course/list/', views.CourseList.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
    path('course/create/', views.CourseCreate.as_view(), name='course_create'),
    path('course/<int:pk>/update', views.CourseUpdate.as_view(), name='course_update'),

    path('subscription/<int:pk>/create/', views.create_subscription, name='create_subscription'),
    path('subscription/<int:pk>/delete/', views.delete_subscription, name='delete_subscription'),

    path('course/lesson/<int:pk>/', views.LessonDetail.as_view(), name='lesson_detail'),
    path('course/<int:pk>/lesson/create/', views.LessonCreate.as_view(), name='lesson_create'),
    path('course/lesson/<int:pk>/update', views.LessonUpdate.as_view(), name='lesson_update'),

    path('course/lesson/<int:pk>/homework/create', views.create_homework, name='create_homework'),
]
