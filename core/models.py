from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

DjangoUser = get_user_model()


class User(DjangoUser):
    class Meta:
        proxy = True


def avatar_directory_path(instance: models.Model, filename: str) -> str:
    # файл сохранится в MEDIA_ROOT/user_<id>/<filename>
    return 'avatar/user_{0}/{1}'.format(instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    first_name = models.CharField('Имя', max_length=255)
    last_name = models.CharField('Фамилия', max_length=255)
    patronymic = models.CharField('Отчество', max_length=255, blank=True)
    birthday = models.DateField('День рождения', null=True, blank=True)
    avatar = models.ImageField(upload_to=avatar_directory_path, blank=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    @property
    def full_name(self) -> str:
        return ' '.join(filter(bool, [self.first_name, self.last_name, self.patronymic]))

    @property
    def only_names(self) -> str:
        return f'{self.last_name.capitalize()} {self.first_name.capitalize()}'

    def get_avatar(self) -> str:
        if self.avatar:
            return self.avatar.url
        return '/static/core/img/no_image.png'

    def __str__(self) -> str:
        return self.full_name
