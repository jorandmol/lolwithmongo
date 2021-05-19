from bs4 import BeautifulSoup
import urllib.request
import datetime
import re

URL_BASE = "https://lol.fandom.com"
INITIAL_YEAR = 2018
NO_DATA = "Sin datos"
REGIONS = ["LCS","LEC","LCK","LPL","NA LCS","EU LCS"]

def get_team_clas(standings):
    res = []
    qualifyng = standings.find("table", class_="wikitable2 standings").find_all("tr", class_="teamhighlight")
    for pos in qualifyng:
        team_name = pos["data-teamhighlight"]
        team_data = pos.find_all("td")
        team_pos = team_data[0].get_text()
        team_res = team_data[2].get_text()
        team_vic = team_data[3].get_text()
        res.append((team_pos,team_name,team_res,team_vic))
    return res

class LoL_pedia():

    competitions = []
    splits = []

    def get_data(self):
        self.get_competitions()
        print("Se han almacenado " + len(self.competitions) + " competiciones en total")
        self.get_splits()
        print("con sus respectivos " + len(self.splits) + " splits")

    def get_competitions(self):
        year_now = datetime.datetime.now().year
        i = INITIAL_YEAR
        comp = []
        while i < year_now+1:
            f = urllib.request.urlopen(URL_BASE+"/wiki/"+str(i)+"_Season")
            s = BeautifulSoup(f, "lxml")
            content = s.find("div", id="global-wrapper").find("div", id="pageWrapper").find(id="bodyContent")
            tabla = content.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find("div", class_="mw-parser-output").find("table", class_="frontpagetable")
            domestic_list = tabla.tbody.find_all("tr")[2].find("table", class_="navbox").find("table", class_="nowraplinks").tbody.find_all("tr")[4].find("div", class_="hlist").find_all("li")
            for region in domestic_list:
                reg_link = region.find("a")
                if reg_link.get_text() in REGIONS:
                    comp_url = URL_BASE+reg_link["href"]
                    comp_name = reg_link.get_text()
                    season_year = str(i)
                    comp.append((season_year,comp_name,comp_url))
            i += 1
        self.competitions = comp

    def get_splits(self):
        splits = []
        for comp in self.competitions:
            f = urllib.request.urlopen(comp[2])
            s = BeautifulSoup(f, "lxml")
            content = s.find("div", id="global-wrapper").find("div", id="pageWrapper").find(id="bodyContent")
            data = content.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find("div", class_="mw-parser-output").find_all("h2")[:2]
            for split in data:
                split_name = split.find("span").get_text()
                clas = []
                knock = []
                standings = split.next_sibling.next_sibling
                clasif = get_team_clas(standings)
                clas = clasif
                if comp[1] == "LPL" and comp[0] == "2018":
                    standings = standings.next_sibling.next_sibling
                    clasif = get_team_clas(standings)
                    clas.extend(clasif)
                knockout = standings.next_sibling.next_sibling
                rounds = knockout.find_all("div", {"class": re.compile("^bracket-team round\d teamhighlight teamhighlighter")})
                for team in rounds:
                    if team.has_attr("data-teamhighlight"):
                        r_team_name = team["data-teamhighlight"]
                        points = team.find("div", class_="bracket-team-points").get_text()
                        round = re.search("round\d", str(team["class"]))
                        knock.append((round.group(0),r_team_name,points))
                splits.append((comp[0],comp[1],split_name,clas,knock))
        self.splits = splits