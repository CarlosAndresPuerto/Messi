# Generated by Django 4.2.7 on 2023-12-13 06:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_customuser_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='identity',
            field=models.IntegerField(null=True, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(99999999999)]),
        ),
    ]