from django.contrib import admin
from .models import ComprobantesRecibidos

class ComprobantesRecibidosAdmin(admin.ModelAdmin):
    list_display = ('Fecha','Tipo','Punto_de_Venta','Numero_Desde','Cuit','Denominacion_Emisor','Total_pesos')
    readonly_fields = ('created', 'updated')
    search_fields = ('Denominacion_Emisor','Cuit','Numero_Desde','Moneda')
    date_hierarchy = 'Fecha'
    list_filter = ('Contribuyente',)

admin.site.register(ComprobantesRecibidos,ComprobantesRecibidosAdmin)

