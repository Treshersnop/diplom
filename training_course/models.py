from django.db import models

from training_course import consts


class Category(models.Model):
    name = models.CharField('Название', max_length=255, unique=True)
    parent_category = models.ManyToManyField(
        'self',
        related_name='children',
        symmetrical=False,
        verbose_name='Родительская категория',
        blank=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.name


def image_directory_path(instance: models.Model, filename: str) -> str:
    # файл сохранится в MEDIA_ROOT/user_<id>/<filename>
    return 'course_image/course_{0}/{1}'.format(instance.id, filename)


class TrainingCourse(models.Model):
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, verbose_name='Категория', related_name='courses', on_delete=models.SET_NULL, null=True, blank=True
    )

    responsible = models.ManyToManyField(
        'core.User', verbose_name='Ответственные', related_name='responsible_for_courses', blank=True
    )

    from_data = models.DateField('Начало курса', help_text='С какого числа начинается курс',
                                 null=True, blank=True)
    to_data = models.DateField('Окончание курса', help_text='Какого числа заканчивается курс',
                               null=True, blank=True)

    level = models.CharField(
        'Уровень сложности', max_length=255, choices=consts.LEVEL_CHOICES, default=consts.LEVEL_FOR_BEGINNERS
    )
    is_active = models.BooleanField('Активен', default=True)
    number_of_clicks = models.PositiveIntegerField('Количество нажатий на курс', default=0)
    image = models.ImageField(upload_to=image_directory_path, blank=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self) -> str:
        return self.name

    def get_data(self) -> str:
        data = ''
        if self.from_data:
            data = f'с {self.from_data.strftime("%d.%m.%Y")}'
            if self.to_data:
                data += f' по {self.to_data.strftime("%d.%m.%Y")}'
        elif self.to_data:
            data = f'до {self.to_data.strftime("%d.%m.%Y")}'
        return data

    def get_image(self) -> str:
        if self.image:
            return self.image.url
        return '/static/training_course/img/no_image.webp'


class Lesson(models.Model):
    name = models.CharField('Название', max_length=255)
    course = models.ForeignKey(
        TrainingCourse, verbose_name='К курсу', related_name='lessons', on_delete=models.CASCADE, null=True, blank=True
    )
    description = models.TextField('Описание', blank=True)
    link = models.URLField('Ссылка на внешний сервис', blank=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self) -> str:
        return f'{self.name} к курсу {self.course}'


class LessonFile(models.Model):
    name = models.CharField('Название', max_length=255)
    lesson = models.ForeignKey(Lesson, verbose_name='К уроку', related_name='files', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to='lesson_media')

    class Meta:
        verbose_name = 'Файл урока'
        verbose_name_plural = 'Файлы урока'

    def __str__(self) -> str:
        return f'{self.name} к уроку {self.lesson}'

    def get_absolute_file_url(self) -> str:
        return self.file.url


class Subscription(models.Model):
    course = models.ForeignKey(
        TrainingCourse, verbose_name='Курс', related_name='subscriptions', on_delete=models.CASCADE
    )
    dc = models.DateTimeField('Дата приобретения', auto_now_add=True)
    user = models.ForeignKey(
        'core.User', verbose_name='Пользователь', related_name='subscriptions', on_delete=models.CASCADE
    )
    is_blocked = models.BooleanField('Заблокирована', default=False)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self) -> str:
        return self.course.name


class Test(models.Model):
    lesson = models.OneToOneField(Lesson, verbose_name='К тесту', related_name='test', on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self) -> str:
        return f'Тест к уроку {self.lesson.name}'


class Question(models.Model):
    test = models.ForeignKey(Test, verbose_name='К тесту', related_name='questions', on_delete=models.CASCADE)
    name = models.TextField('Вопрос')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self) -> str:
        return f'Вопрос к тесту {self.test.lesson.name}'


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='К вопросу', related_name='answers', on_delete=models.CASCADE)
    name = models.TextField('Ответ')
    is_right = models.BooleanField('Верный', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self) -> str:
        return f'Ответ к вопросу {self.question.name}'


class Task(models.Model):
    lesson = models.OneToOneField(
        Lesson, verbose_name='К уроку', related_name='task', on_delete=models.PROTECT
    )
    name = models.CharField('Название', max_length=255)
    description = models.TextField('Описание', blank=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self) -> str:
        return self.name


class TaskFile(models.Model):
    name = models.CharField('Название', max_length=255)
    task = models.ForeignKey(Task, verbose_name='К задаче', related_name='files', on_delete=models.CASCADE)
    file = models.FileField('Файл', upload_to='task_media')

    class Meta:
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задач'

    def __str__(self) -> str:
        return f'{self.name} к уроку {self.task}'

    def get_absolute_file_url(self) -> str:
        return self.file.url


class Homework(models.Model):
    learner = models.ForeignKey(
        'core.User', verbose_name='Сдавший ученик', related_name='homeworks', on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task, verbose_name='К задаче', related_name='homeworks', on_delete=models.CASCADE
    )
    description = models.TextField('Описание', blank=True)
    is_checked = models.BooleanField('Проверено преподавателем', default=False)

    class Meta:
        verbose_name = 'Домашнее задание'
        verbose_name_plural = 'Домашние задания'

    def __str__(self) -> str:
        return f'{self.learner} к задаче {self.task}'


class HomeworkFile(models.Model):
    name = models.CharField('Название', max_length=255)
    homework = models.ForeignKey(
        Homework, verbose_name='К д/з', related_name='files', on_delete=models.CASCADE
    )
    file = models.FileField('Файл', upload_to='homework_media')

    class Meta:
        verbose_name = 'Файл д/з'
        verbose_name_plural = 'Файлы д/з'

    def __str__(self) -> str:
        return f'{self.name} к д/з {self.homework}'

    def get_absolute_file_url(self) -> str:
        return self.file.url
