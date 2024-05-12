# Generated by Django 5.0.3 on 2024-04-21 17:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('training_course', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainingcourse',
            old_name='admission_how_days',
            new_name='days_admission',
        ),
        migrations.RemoveField(
            model_name='trainingcourse',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='category',
            name='parent_category',
        ),
        migrations.RemoveField(
            model_name='lesson',
            name='viewed_users',
        ),
        migrations.AlterField(
            model_name='lessonfile',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='training_course.lesson', verbose_name='К уроку'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='is_blocked',
            field=models.BooleanField(default=False, verbose_name='Заблокирована'),
        ),
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('is_checked', models.BooleanField(default=False, verbose_name='Проверено преподавателем')),
                ('learner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='core.user', verbose_name='Сдавший ученик')),
            ],
            options={
                'verbose_name': 'Домашнее задание',
                'verbose_name_plural': 'Домашние задания',
            },
        ),
        migrations.CreateModel(
            name='HomeworkFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('file', models.FileField(upload_to='homework_media', verbose_name='Файл')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='training_course.homework', verbose_name='К д/з')),
            ],
            options={
                'verbose_name': 'Файл д/з',
                'verbose_name_plural': 'Файлы д/з',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='training_course.lesson', verbose_name='К уроку')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
        migrations.AddField(
            model_name='homework',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homeworks', to='training_course.task', verbose_name='К задаче'),
        ),
        migrations.CreateModel(
            name='TaskFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('file', models.FileField(upload_to='task_media', verbose_name='Файл')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='training_course.task', verbose_name='К задаче')),
            ],
            options={
                'verbose_name': 'Файл задачи',
                'verbose_name_plural': 'Файлы задач',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ManyToManyField(blank=True, related_name='children', to='training_course.category', verbose_name='Родительская категория'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='viewed_users',
            field=models.ManyToManyField(blank=True, related_name='viewed_lessons', to='core.user', verbose_name='Просмотревшие пользователи'),
        ),
    ]
