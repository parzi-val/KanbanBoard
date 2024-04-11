# Generated by Django 4.2.6 on 2024-04-10 00:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_remove_project_id_alter_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boards', to='backend.project'),
        ),
    ]
