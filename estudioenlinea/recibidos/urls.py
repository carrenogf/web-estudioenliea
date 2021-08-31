from django.urls import path
from .views import MisComprobantesRecibidosView, recibidos_succes

urlpatterns = [
    path('recibidos/',MisComprobantesRecibidosView , name="recibidos"),
    path('recibidos_succes/',recibidos_succes,name="recibidos_succes"),
]