# Generated by Django 4.2.6 on 2024-04-10 23:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('backend', '0011_alter_task_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='reporter',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='reported_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
