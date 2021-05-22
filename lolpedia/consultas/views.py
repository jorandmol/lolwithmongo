from django.shortcuts import render,redirect
from django.urls import reverse
from urllib.parse import urlencode
from django.views.generic import TemplateView
from consultas.scrapping import  LoL_pedia
from consultas.models import Position,Season,Split,Match,Round,League


class ConsultasView(TemplateView):
    template_name = 'buscador.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['seasons'] = Season.objects.all()

            return context

        except Exception:
            context = {'error_message': 'Ha ocurrido un error inesperado'}
            return render(self.request, 'base/error.html', context)

class LeagueView(TemplateView):
    template_name = 'league.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            league_id = self.kwargs.get('pk')
            league = League.objects.get(id=int(league_id))
            # Stats
            stats = []
            for split in league.split_set.all():
                n_rounds = split.round_set.count()
                more_wins = split.position_set.all().order_by('-wins')[0]
                more_loses = split.position_set.all().order_by('-loses')[0]
                if n_rounds > 0:
                    final = split.round_set.all()[n_rounds-1]
                    final_game = final.match_set.all()[0]
                    result = final_game.result.split(" - ")
                    if int(result[0]) >  int(result[1]):
                        winner = final_game.home
                    else:
                        winner = final_game.visitor
                else:
                    winner = "-"
                stats.append((more_wins,more_loses,winner))

            context['league'] = league
            context['stats'] = stats

            return context

        except Exception:
            context = {'message': 'There was an error'}
            return render(self.request, 'buscador.html', context)

def CargaDatos(request):
    bd = LoL_pedia()
    try:
        bd.get_data()
        l_dict = carga_seasons(bd)
        carga_splits(l_dict,bd)
        message = "Load data completed"
        return redirect("/")
    except:
        message = "Data could not be stored"
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
            r_name = r.replace("round","Round ")
            round = Round(name=r_name,split=split)
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

