# Generated by Django 4.2.7 on 2023-12-07 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_customuser_is_teacher_candidate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_teacher_candidate',
            field=models.BooleanField(default=False),
        ),
    ]
