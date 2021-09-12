from django.contrib import admin
from .models import Contribuyente, Notificaciones

# Register your models here.
class ContribuyenteAdmin(admin.ModelAdmin):
    list_display = ('Razon_Social', 'Cuit', 'Usuario')
    readonly_fields = ('created', 'updated')
    search_fields = ('Razon_Social','Cuit','Usuario')
    

class NotificacionesAdmin(admin.ModelAdmin):
    list_display = ('Titulo', 'Mensaje', 'created')
    readonly_fields = ('created', 'updated')
    search_fields = ('Titulo','Mensaje')
    list_filter = ('Contribuyente',)

admin.site.register(Contribuyente, ContribuyenteAdmin)
admin.site.register(Notificaciones, NotificacionesAdmin)
