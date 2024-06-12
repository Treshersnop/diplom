from django import template

from training_course import models

register = template.Library()


@register.filter
def user_has_subscription(course: models.TrainingCourse, user_id: int) -> bool:
    return course.subscriptions.filter(user_id=user_id).exists()


@register.filter
def is_user_responsible_for_course(course: models.TrainingCourse, user_id: int) -> bool:
    return course.responsible.filter(id=user_id).exists()


@register.filter
def does_user_do_homework(lesson: models.Lesson, user_id: int) -> bool:
    if task := lesson.task:
        return (
            task.homeworks.filter(learner_id=user_id).exists() or lesson.course.responsible.filter(id=user_id).exists()
        )
