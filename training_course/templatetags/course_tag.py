from django import template

from training_course import models

register = template.Library()


@register.filter
def user_has_subscription(course: models.TrainingCourse, user_id: int) -> bool:
    return course.subscriptions.filter(user_id=user_id).exists()


@register.filter
def is_user_responsible_for_course(course: models.TrainingCourse, user_id: int) -> bool:
    return course.responsible.filter(id=user_id).exists()
