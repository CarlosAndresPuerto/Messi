# Generated by Django 4.2.5 on 2023-11-14 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_usercustom_is_superadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='task_attachments/'),
        ),
    ]
