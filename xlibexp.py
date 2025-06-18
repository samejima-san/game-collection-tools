import requests
import os
import psycopg2
from bs4 import BeautifulSoup
from dotenv import load_dotenv
load_dotenv()

conn= psycopg2.connect(
    dbname=os.getenv("DBNAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host="localhost",
    port="5432"
)


gamertag = os.getenv("GAMERTAG")
gamerid = os.getenv("GAMER_ID")
url = f"https://www.trueachievements.com/gamer/{gamertag}/games"
counter = 1

url3 = (
    f"https://www.trueachievements.com/gamer/{gamertag}/games?"
    "function=AjaxList"
    "&params=oGamerGamesList|"
    f"&oGamerGamesList_Page={counter}"
    "&oGamerGamesList_ItemsPerPage=400"
    "oGamerGamesList_ShowAll=True"
)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"
}
responselist = []
urllist = []
games = []
puregamelist = []

def getListOfGames():
    response = requests.get(url3, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    end = soup.find(class_='l').a.text.strip()
    end = int(end)
    for counter in range(1, end+1):
        urllist.append(
            f"https://www.trueachievements.com/gamer/{gamertag}/games?function=AjaxList&params=oGamerGamesList|&oGamerGamesList_Page={counter}&oGamerGamesList_ItemsPerPage=400oGamerGamesList_ShowAll=True"
        )

    for url in urllist:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        responselist.append(soup)
    
    for response in responselist:
        games.append(response.find_all(class_='smallgame'))

    for game in games:
        for arr in game:
            puregamelist.append((arr.text, arr.find("a").get("href", "").strip()))

    return puregamelist

def update_gametime():
    cur = conn.cursor()
    cur.execute("SELECT vg_name, hours_played, finished FROM lib;")

    games = cur.fetchall()
    gamehash = {}
    xboxlibrary = getListOfGames()
    xboxhash = {}

    for game in xboxlibrary:
        xboxhash[game[0]]= game[1] #vg_name  link


