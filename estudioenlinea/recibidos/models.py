from django.db import models
from django.db.models.deletion import CASCADE
from contribuyente.models import Contribuyente

class ComprobantesRecibidos(models.Model):
    Contribuyente = models.ForeignKey(Contribuyente, on_delete=models.CASCADE)
    Fecha=models.DateField()
    Tipo=models.CharField(max_length=60)
    Punto_de_Venta=models.IntegerField(verbose_name="Pto. Vta")
    Numero_Desde=models.IntegerField( verbose_name= "N° comp")
    Cuit=models.IntegerField()
    Denominacion_Emisor=models.CharField(max_length=120, verbose_name="Razón Social")
    Tipo_Cambio=models.DecimalField(decimal_places=2,max_digits=20,default=1)
    Moneda=models.CharField(max_length=120,default="$")
    Imp_Neto_Gravado=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    Imp_Neto_No_Gravado=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    Imp_Op_Exentas=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    IVA=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    Imp_Total=models.DecimalField(decimal_places=2,max_digits=20,default=0)
    Neto_pesos=models.DecimalField(decimal_places=2,max_digits=20)
    Iva_pesos=models.DecimalField(decimal_places=2,max_digits=20)
    Total_pesos=models.DecimalField(decimal_places=2,max_digits=20)
    Alicuota=models.DecimalField(decimal_places=2,max_digits=5)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        verbose_name = "Comprobante Recibido"
        verbose_name_plural = "Comprobantes Recibidos"
        ordering = ["-Fecha"]
