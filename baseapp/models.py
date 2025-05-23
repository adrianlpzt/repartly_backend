from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=100, default='avatar1.png')  # nombre del archivo
    fecha_nacimiento = models.DateField(null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    notas = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    nif = models.CharField(max_length=20, blank=True)


    def __str__(self):
        return self.user.username

class Platform(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='platforms')
    nombre = models.CharField(max_length=100)
    precio_entrega = models.DecimalField(max_digits=6, decimal_places=2)
    precio_recogida = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.nombre} ({self.user.username})"
    
class Entrega(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entregas')
    plataforma = models.ForeignKey(Platform, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Entrega de {self.cantidad} en {self.plataforma.nombre} - {self.user.username}"

class Recogida(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recogidas')
    plataforma = models.ForeignKey(Platform, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    total = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Recogida de {self.cantidad} en {self.plataforma.nombre} - {self.user.username}"

class Gasto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gastos')
    concepto = models.CharField(max_length=100)
    cantidad = models.DecimalField(max_digits=7, decimal_places=2)
    observaciones = models.TextField(blank=True, null=True)
    fecha = models.DateField()

    def __str__(self):
        return f"Gasto: {self.concepto} - {self.cantidad} € ({self.user.username})"
