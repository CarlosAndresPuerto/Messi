# Generated by Django 4.2.5 on 2023-11-17 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_entregatarea_informacion_adicional_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entregatarea',
            name='informacion_adicional',
        ),
        migrations.RemoveField(
            model_name='task',
            name='informacion_adicional',
        ),
    ]
