# Generated by Django 4.2.7 on 2023-12-13 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_customuser_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='identity',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]
