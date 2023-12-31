# Generated by Django 4.2.5 on 2023-11-15 02:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NuevoRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('Nombres', models.CharField(max_length=100)),
                ('Apellidos', models.CharField(max_length=100)),
                ('Clave', models.CharField(max_length=128)),
                ('NumeroCuenta', models.CharField(blank=True, max_length=20, null=True)),
                ('SaldoContable', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('SaldoCuentaCorriente', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('SaldoLineaCredito', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TotalCargos', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('TotalAbonos', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('Estado', models.BooleanField(default=True)),
                ('intentos_fallidos', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='SecurityAudit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('event_type', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='iniciar.nuevoregistro')),
            ],
        ),
    ]
