from django.db import models


class Room(models.Model):
    name = models.CharField('Название', max_length=255)
    participants = models.ManyToManyField(
        'core.User', verbose_name='Участники чата', related_name='rooms', blank=True
    )
    is_group = models.BooleanField('Является групповой перепиской', default=True)

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    room = models.ForeignKey(Room, verbose_name='Чат', related_name='messages', on_delete=models.CASCADE)
    description = models.TextField('Описание', blank=True)
    dc = models.DateTimeField('Время отправления', auto_now_add=True)
    sender = models.ForeignKey(
        'core.User', verbose_name='Отправитель', related_name='messages', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self) -> str:
        return self.description


class MessageFile(models.Model):
    name = models.CharField('Название', max_length=255)
    message = models.ForeignKey(Message, verbose_name='К сообщению', related_name='files', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to='message_media')

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self) -> str:
        return f'{self.name} к сообщению {self.message.id}'
