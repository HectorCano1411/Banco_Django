# Generated by Django 4.2.5 on 2023-09-13 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniciar', '0007_remove_nuevoregistro_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nuevoregistro',
            name='rut',
            field=models.CharField(max_length=12, unique=True),
        ),
    ]