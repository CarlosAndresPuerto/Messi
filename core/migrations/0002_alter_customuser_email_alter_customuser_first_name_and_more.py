# Generated by Django 4.2.7 on 2023-12-04 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=30, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='identity',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='teacher_password',
            field=models.CharField(blank=True, max_length=18, null=True),
        ),
    ]
