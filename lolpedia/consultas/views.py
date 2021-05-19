from django.shortcuts import render
from django.views.generic import TemplateView
from consultas.scrapping import  LoL_pedia
from consultas.models import Position,Season,Split,Match,Round,League


class ConsultasView(TemplateView):
    template_name = 'buscador.html'

def CargaDatos(request):
    bd = LoL_pedia()
    try:
        bd.get_data()
        carga_seasons(bd)
        message = "La carga se ha realizado de manera satisfactoria"
    except:
        message = "No se ha podido cargar la base de datos"
    return render(request, 'buscador.html', {'message': message})

def carga_seasons(bd):
    Season.objects.all().delete()
    League.objects.all().delete()
    registros = bd.competitions
    l_dict = {}
    for reg in registros:
        season, created = Season.objects.get_or_create(year=int(reg[0]))
        if not created:
            season.save()
        league = League(season=season,name=reg[1])
        league.save()
        id = str(season.year)+"-"+reg[1]
        l_dict[id] = league
    print("Se han almacenado " + str(len(l_dict)) + " ligas")
    return l_dict

def carga_splits(l_dict):
    Match.objects.all().delete()
    Position.objects.all().delete()
    Round.objects.all().delete()
    Split.objects.all().delete()

