from django.urls import path

from training_course.views import course

app_name = 'training_course'

urlpatterns = [
    path('course/list/', course.CourseList.as_view(), name='course_list'),
    path('course/<int:pk>', course.CourseDetail.as_view(), name='course_detail'),
    path('course/create', course.CourseCreate.as_view(), name='course_create'),
]
