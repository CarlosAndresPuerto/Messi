# Generated by Django 4.2.7 on 2023-12-13 05:39

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='identity',
            field=models.IntegerField(null=True, unique=True, validators=[django.core.validators.MinLengthValidator(5), django.core.validators.MaxLengthValidator(15)]),
        ),
    ]