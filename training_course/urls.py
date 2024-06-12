from django.urls import path

from training_course import views

app_name = 'training_course'

urlpatterns = [
    path('course/list/', views.CourseList.as_view(), name='course_list'),
    path('course/<int:pk>/', views.CourseDetail.as_view(), name='course_detail'),
    path('course/create/', views.CourseCreate.as_view(), name='course_create'),
    path('course/<int:pk>/update/', views.CourseUpdate.as_view(), name='course_update'),
    path('course/<int:pk>/statistic/', views.CourseStatistic.as_view(), name='course_statistic'),
    path('course/<int:pk>/delete/', views.CourseDelete.as_view(), name='course_delete'),
    path('subscription/<int:pk>/create/', views.SubscriptionCreate.as_view(), name='create_subscription'),
    path('subscription/<int:pk>/delete/', views.SubscriptionDelete.as_view(), name='delete_subscription'),
    path('course/lesson/<int:pk>/', views.LessonDetail.as_view(), name='lesson_detail'),
    path('course/<int:pk>/lesson/create/', views.LessonCreate.as_view(), name='lesson_create'),
    path('course/lesson/<int:pk>/update/', views.LessonUpdate.as_view(), name='lesson_update'),
    path('course/lesson/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson_delete'),
    path('course/lesson/task/<int:pk>/homework/create/', views.HomeworkCreate.as_view(), name='homework_create'),
    path('course/lesson/task/homework/<int:pk>/update/', views.HomeworkUpdate.as_view(), name='homework_update'),
    path('course/lesson/task/homework/<int:pk>/check/', views.check_homework, name='homework_check'),
]
