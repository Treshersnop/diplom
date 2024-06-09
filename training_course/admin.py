from django.contrib import admin

from training_course import models


@admin.register(models.Category)
class Category(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(models.TrainingCourse)
class TrainingCourse(admin.ModelAdmin):
    list_display = ('name', 'category', 'level', 'is_active')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'from_data', 'to_data')


@admin.register(models.Lesson)
class Lesson(admin.ModelAdmin):
    list_display = ('name', 'course')
    search_fields = ('name',)


@admin.register(models.LessonFile)
class LessonFile(admin.ModelAdmin):
    list_display = ('name', 'lesson',)


@admin.register(models.Test)
class Test(admin.ModelAdmin):
    list_display = ('lesson',)
    search_fields = ('lesson__name',)


@admin.register(models.Question)
class Question(admin.ModelAdmin):
    list_display = ('name', 'test',)
    search_fields = ('name', 'test__lesson__name',)


@admin.register(models.Answer)
class Answer(admin.ModelAdmin):
    list_display = ('name', 'question', 'is_right')
    search_fields = ('name', 'question__name', 'question__test__lesson__name')


@admin.register(models.TaskFile)
class TaskFile(admin.ModelAdmin):
    list_display = ('name', 'task',)


@admin.register(models.Homework)
class Homework(admin.ModelAdmin):
    list_display = ('learner', 'task', 'is_checked')
    list_filter = ('is_checked',)


@admin.register(models.HomeworkFile)
class HomeworkFile(admin.ModelAdmin):
    list_display = ('name', 'homework',)


@admin.register(models.Subscription)
class Subscription(admin.ModelAdmin):
    list_display = ('course', 'user', 'is_blocked')
    search_fields = ('course__name', 'user__profile__last_name', 'user__profile__name')
    list_filter = ('is_blocked',)
