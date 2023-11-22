# Generated by Django 4.2.5 on 2023-11-15 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('iniciar', '0002_nuevoregistro_tipocuenta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo', models.CharField(choices=[('corriente', 'Cuenta Corriente'), ('ahorro', 'Cuenta de Ahorro')], default='corriente', max_length=10)),
                ('titular', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iniciar.nuevoregistro')),
            ],
        ),
        migrations.CreateModel(
            name='Transferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('aprobada', models.BooleanField(default=False)),
                ('referencia', models.CharField(blank=True, max_length=20, null=True)),
                ('detalles', models.JSONField(blank=True, null=True)),
                ('tasa_interes', models.FloatField(blank=True, null=True)),
                ('motivo_rechazo', models.CharField(blank=True, max_length=100, null=True)),
                ('cuenta_destino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuenta_destino', to='transferencias.cuenta')),
                ('cuenta_origen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cuenta_origen', to='transferencias.cuenta')),
            ],
        ),
    ]
