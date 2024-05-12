# Generated by Django 5.0.3 on 2024-03-26 12:49

import core.models
import django.contrib.auth.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('patronymic', models.CharField(blank=True, max_length=255, verbose_name='Отчество')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='День рождения')),
                ('avatar', models.ImageField(blank=True, upload_to=core.models.avatar_directory_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='profile', to='core.user')),
            ],
            options={
                'verbose_name': 'Профиль пользователя',
                'verbose_name_plural': 'Профили пользователей',
            },
        ),
    ]
