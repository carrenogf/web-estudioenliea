from django.urls import path
from .views import perfil, resumen, resumen_success, NotificacionesDetailView, NotificacionesListView

urlpatterns = [
    path('perfil/',perfil, name="perfil"),
    path('notificaciones/',NotificacionesListView.as_view(),name = 'notificaciones'),
    path('notificacion/<int:pk>/',NotificacionesDetailView.as_view(), name='notificacion'),
    path('resumen/',resumen , name="resumen"),
    path('resumen_success/',resumen_success , name="resumen_success"),
]