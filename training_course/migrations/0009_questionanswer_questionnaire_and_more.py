# Generated by Django 5.0.3 on 2024-06-10 06:31

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('training_course', '0008_question_answer_test_question_test'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(related_name='question_questionnaires', to='training_course.answer', verbose_name='Ответы')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_questionnaires', to='training_course.question', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вопрос-ответ',
                'verbose_name_plural': 'Вопросы-ответы',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Результат (в %)')),
                ('questions', models.ManyToManyField(through='training_course.QuestionAnswer', to='training_course.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questionnaires', to='core.user', verbose_name='Прошедший')),
            ],
            options={
                'verbose_name': 'Опросник',
                'verbose_name_plural': 'Опросники',
            },
        ),
        migrations.AddField(
            model_name='questionanswer',
            name='questionnaire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_answers', to='training_course.questionnaire', verbose_name='К опроснику'),
        ),
    ]
