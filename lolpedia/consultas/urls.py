from django.urls import path
from .views import CargaDatos, ConsultasView, LeagueView


urlpatterns = [
    path('', ConsultasView.as_view(), name='consultas'),
    path('carga_bd', CargaDatos, name='cargar'),
    path('league/<pk>', LeagueView.as_view(), name='league')
]