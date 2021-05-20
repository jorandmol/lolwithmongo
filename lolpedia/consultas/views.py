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
        l_dict = carga_seasons(bd)
        carga_splits(l_dict,bd)
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

def carga_splits(l_dict,bd):
    Match.objects.all().delete()
    Position.objects.all().delete()
    Round.objects.all().delete()
    Split.objects.all().delete()
    registros = bd.splits
    for reg in registros:
        id = reg[0]+"-"+reg[1]
        split = Split(name=reg[2],league=l_dict[id])
        split.save()
        # Standings
        for pos in reg[3]:
            result = pos[2].split("-")
            wins = result[0].strip()
            loses = result[1].strip()
            position = Position(split=split,place=pos[0],team=pos[1],wins=wins,loses=loses)
            position.save()
        # Knockout
        rounds = info_matches(reg[4])
        for r in rounds:
            round = Round(name=r,split=split)
            round.save()
            aux = list(filter(lambda x: x[0]==r,reg[4]))
            n_matches = len(aux)/2
            i = 0
            while i <= n_matches:
                result = aux[i][2]+" - "+aux[i+1][2]
                match = Match(round=round,home=aux[i][1],visitor=aux[i+1][1],result=result)
                match.save()
                i += 2


def info_matches(results):
    res = []
    [res.append(x[0]) for x in results if x[0] not in res]
    return res

