# Generated by Django 4.2.5 on 2023-09-27 23:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_remove_usercustom_identy_usercustom_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercustom',
            name='identity',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(100000000), django.core.validators.MaxValueValidator(9999999999)], verbose_name='Numero de identidad'),
        ),
    ]
