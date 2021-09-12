from django.contrib import admin
from .models import ComprobantesEmitidos

# Register your models here.

class ComprobantesEmitidosAdmin(admin.ModelAdmin):
    list_display = ('Fecha','Tipo','Punto_de_Venta','Numero_Desde','Cuit','Denominacion_Receptor','Total_pesos')
    readonly_fields = ('created', 'updated')
    search_fields = ('Denominacion_Receptor','Cuit','Numero_Desde','Moneda')
    date_hierarchy = 'Fecha'
    list_filter = ('Contribuyente',)


admin.site.register(ComprobantesEmitidos,ComprobantesEmitidosAdmin)

