import django_filters
from django.db.models import Q, QuerySet

from training_course import models


class Course(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Название курса', lookup_expr='icontains')
    responsible = django_filters.CharFilter(label='Создатели курса', method='get_responsible')
    category = django_filters.ModelChoiceFilter(
        label='Категория курса',
        queryset=models.Category.objects.all(),
        empty_label='Все',
    )

    class Meta:
        model = models.TrainingCourse
        fields = ('category',)

    def get_responsible(self, queryset: QuerySet, name: str, value: str) -> QuerySet[models.TrainingCourse]:
        for val in value.split():
            queryset = queryset.filter(
                Q(responsible__profile__first_name__icontains=val)
                | Q(responsible__profile__last_name__icontains=val)
                | Q(responsible__profile__patronymic__icontains=val),
            )
        return queryset
