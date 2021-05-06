from bs4 import BeautifulSoup
import urllib.request

# Funciones para hacer scrapping de la web

URL_BASE = "https://lol.fandom.com"
URL_WORLDS = "_World_Championship"
NO_DATA = "Sin datos"

class LoL_pedia():

    seasons = []

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

if __name__ == "__main__":
    base = LoL_pedia()
    base.get_seasons()