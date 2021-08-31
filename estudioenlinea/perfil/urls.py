from django.urls import path
from .views import perfil, resumen, resumen_success

urlpatterns = [
    path('perfil/',perfil, name="perfil"),
    path('resumen/',resumen , name="resumen"),
    path('resumen_success/',resumen_success , name="resumen_success"),
]