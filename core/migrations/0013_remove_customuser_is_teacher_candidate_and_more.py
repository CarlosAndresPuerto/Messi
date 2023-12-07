# Generated by Django 4.2.7 on 2023-12-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_teacher_approved_by_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_teacher_candidate',
        ),
        migrations.AddField(
            model_name='customuser',
            name='teacher_password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
