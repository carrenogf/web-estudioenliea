from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Contribuyente(models.Model):
    Usuario = models.OneToOneField(User,on_delete=models.CASCADE)
    Razon_Social = models.CharField(max_length=200, verbose_name="Razón Social")
    Cuit = models.IntegerField()
    Actividades = models.TextField(blank=True, null=True,verbose_name="Actividades Económicas")
    Fecha_inicio = models.DateField(verbose_name="Fecha de Inicio de Actividades",blank=True,null=True)
    telefono = models.IntegerField(verbose_name="Teléfono Celular",blank=True, null=True)
    email = models.EmailField(blank=True,null=True)
    observacion = models.TextField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Contribuyente"
        verbose_name_plural = "Contribuyentes"
        ordering = ["-created"]

    def __str__(self):
        return self.Razon_Social