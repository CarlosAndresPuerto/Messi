# Generated by Django 4.2.5 on 2023-11-25 02:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_entregatarea_archivos_adjuntos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entregatarea',
            name='estudiante',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='entregatarea',
            name='tarea',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.task'),
        ),
    ]