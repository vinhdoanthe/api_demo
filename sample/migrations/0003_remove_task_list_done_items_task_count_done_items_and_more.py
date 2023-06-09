# Generated by Django 4.2.1 on 2023-05-09 08:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sample', '0002_remove_task_result_remove_task_task_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='list_done_items',
        ),
        migrations.AddField(
            model_name='task',
            name='count_done_items',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
