from django.urls import path
from .views import MisComprobantesEmitidosView, emitidos_succes

urlpatterns = [
    path('emitidos/',MisComprobantesEmitidosView , name="emitidos"),
    path('emitidos_succes/',emitidos_succes, name="emitidos_succes"),
]