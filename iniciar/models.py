from django.db import models

class Usuario(models.Model):
    Rut = models.CharField(max_length=12)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    Clave = models.CharField(max_length=128)
    NumeroCuenta = models.CharField(max_length=20)
    SaldoContable = models.DecimalField(max_digits=10, decimal_places=2)
    SaldoCuentaCorriente = models.DecimalField(max_digits=10, decimal_places=2)
    SaldoLineaCredito = models.DecimalField(max_digits=10, decimal_places=2)
    TotalCargos = models.DecimalField(max_digits=10, decimal_places=2)
    TotalAbonos = models.DecimalField(max_digits=10, decimal_places=2)
    Estado = models.BooleanField(default=True)
    intentos_fallidos = models.PositiveIntegerField(default=0)  
    def __str__(self):
        return f'Usuario: {self.id} {self.Nombres} {self.Rut} '


class SecurityAudit(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100)
    details = models.TextField()

    
    def __str__(self):
        return f'{self.timestamp} - {self.user.Nombres} {self.user.Apellidos} - {self.event_type}'



from django.db import models

class NuevoRegistro(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    Nombres = models.CharField(max_length=100)
    Apellidos = models.CharField(max_length=100)
    Clave = models.CharField(max_length=128)
    NumeroCuenta = models.CharField(max_length=20, null=True, blank=True)
    SaldoContable = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    SaldoCuentaCorriente = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    SaldoLineaCredito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TotalCargos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    TotalAbonos = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    Estado = models.BooleanField(default=True)
    intentos_fallidos = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'Usuario: {self.id} {self.Nombres} {self.rut} '
