# Generated by Django 4.2.5 on 2023-11-15 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iniciar', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nuevoregistro',
            name='TipoCuenta',
            field=models.CharField(choices=[('corriente', 'Cuenta Corriente'), ('ahorro', 'Cuenta de Ahorro')], default='corriente', max_length=10),
        ),
    ]
