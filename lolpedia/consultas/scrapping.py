from bs4 import BeautifulSoup
import urllib.request

# Funciones para hacer scrapping de la web

URL_BASE = "https://lol.fandom.com"
URL_WORLDS = "_World_Championship"
NO_DATA = "Sin datos"

class LoL_pedia():

    seasons = []
    competitions = []

    def get_seasons(self):
        seasons = []
        f = urllib.request.urlopen(URL_BASE+"/wiki/")
        s = BeautifulSoup(f, "lxml")
        content = s.find("div", id="global-wrapper").find("div", id="pageWrapper").find(id="bodyContent")
        topnav = content.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find("div", class_="mw-parser-output").find("div", class_="frontpage-top")
        seasons_list = topnav.find_all("li")
        for season in seasons_list:
            season_url = URL_BASE+season.a["href"]+URL_WORLDS
            season_year = season.a.get_text()
            seasons.append((season_year,season_url))
        self.seasons = seasons

    def get_competitions_until17(self):
        comp = []
        regions = ["China","South Korea","Europe","North America"]
        for season in self.seasons[1:7]:
            f = urllib.request.urlopen(season[1])
            s = BeautifulSoup(f, "lxml")
            content = s.find("div", id="global-wrapper").find("div", id="pageWrapper").find(id="bodyContent")
            tabla = content.find("div", id="mw-content-text").find("div", class_="mw-parser-output").find("div", class_="mw-parser-output").find("table", class_="navbox").tbody.find("table")
            trows = tabla.find_all("tr")
            for tr in trows:
                if tr.find("td"):
                    region = tr.find("td").get_text()
                    if region in regions:
                        datos_comp = tr.find("td").next_sibling.find_all("li")
                        for c in datos_comp:
                            d = c.a
                            comp.append((season[0],region,d.get_text(),d["href"]))
        self.competitions = comp