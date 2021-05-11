from django.shortcuts import render
from django.views.generic import TemplateView


class ConsultasView(TemplateView):
    template_name = 'buscador.html'

