# Generated by Django 4.2.5 on 2023-11-15 08:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('iniciar', '0002_nuevoregistro_tipocuenta'),
        ('transferencias', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transferencia',
            name='cuenta_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_destino', to='iniciar.nuevoregistro'),
        ),
        migrations.AlterField(
            model_name='transferencia',
            name='cuenta_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transferencias_origen', to='iniciar.nuevoregistro'),
        ),
    ]
