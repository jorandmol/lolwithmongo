from django.urls import path
from .views import CargaDatos, ConsultasView


urlpatterns = [
    path('', ConsultasView.as_view(), name='consultas'),
    path('carga_bd', CargaDatos, name='cargar'),
]