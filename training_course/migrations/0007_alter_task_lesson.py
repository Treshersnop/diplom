# Generated by Django 5.0.3 on 2024-05-21 16:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_course', '0006_remove_subscription_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='lesson',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='task', to='training_course.lesson', verbose_name='К уроку'),
        ),
    ]