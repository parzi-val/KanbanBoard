# Generated by Django 4.2.6 on 2024-04-11 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_task_reporter_alter_task_assigned'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='priority',
            field=models.CharField(choices=[('high', 'High'), ('medium', 'Medium'), ('LOW', 'Low')], max_length=20, null=True),
        ),
    ]
