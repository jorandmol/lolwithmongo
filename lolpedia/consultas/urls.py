from django.urls import path
from .views import ConsultasView


urlpatterns = [
    path('', ConsultasView.as_view(), name='consultas'),
]