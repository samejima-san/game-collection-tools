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
    cur.execute("SELECT vg_name, hours_played, finished, year_played FROM lib;")

    games = cur.fetchall() #vg_name hours_played finished, year_played
    gamehash = {}
    xboxlibrary = getListOfGames()
    xboxhash = {}

    for game in xboxlibrary:
        xboxhash[game[0]] = game[1] #vg_name  link
    
    for game in games:
        gamehash[game[0]] = (game[1], game[2], game[3])# vg_name (hours_played, finished, year_played)

    output = []
    fileoutput = ""
    for key, value in xboxhash.items():
        if key not in gamehash:
            #add it to the .xboxoutput file for not
            output.append([key.replace("'","''"), getLinkInfo(value)]) #year_played, time_played, is_finished, is_completed
        if key in gamehash:
            rep = requests.get("https://www.trueachievements.com"+value, headers=headers)
            var = BeautifulSoup(rep.text, "lxml")
            if gamehash[key][2] == None:
                fileoutput+=f"UPDATE lib SET year_played = {getYearPlayed(var)} WHERE vg_name = '{key.replace("'","''")}';\n"
            time = getTimePlayed(var)
            if gamehash[key][0]<time:
                fileoutput+=f"UPDATE lib SET hours_played = {time} WHERE vg_name = '{key.replace("'","''")}';\n"
                


    if len(output) >= 1:
        fileoutput+="INSERT INTO lib(vg_name, year_played, hours_played, finished, completed)\nVALUES"
    if len(output) == 1:
        fileoutput+=f"('{output[0][0]}',{output[0][1][0]},{output[0][1][1]},{output[0][1][2]},{output[0][1][3]});"#output[fullfile, 0/1, 0/3] name/info   year/hours/complete/finish 
    elif len(output) > 1:
        for i in range(len(output)-2):
            fileoutput+=f"('{output[i][0]}',{output[i][1][0]},{output[i][1][1]},{output[i][1][2]},{output[i][1][3]}),\n"#output[fullfile, 0/1, 0/3] name/info   year/hours/complete/finish 
        fileoutput+=f"('{output[-1][0]}',{output[-1][1][0]},{output[-1][1][1]},{output[-1][1][2]},{output[-1][1][3]});"#output[fullfile, 0/1, 0/3] name/info   year/hours/complete/finish 
    if(len(fileoutput) == 0): return
    
    with open('.xbox_query', "w") as f:
        f.write(fileoutput)

        cur.close()

def getLinkInfo(value):
    link = "https://www.trueachievements.com"+ value
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    year_played = getYearPlayed(soup) #4 digit year
    time_played = getTimePlayed(soup) #hours_played or None
    is_finished = getFinished(soup)#returns true or False
    is_completed = getCompleted(soup)#returns true or false 
    if is_completed == True: is_finished = True #when the game is completed the tag needed for finished isnt there
    return [year_played, time_played, is_finished, is_completed]

def getYearPlayed(html):
    firstplayed = html.find("span",{"title":"First played"})
    firstplayed =firstplayed.text
    if firstplayed is None or len(firstplayed)<=3:
        return 0
    concat = "20"+firstplayed[-2:]
    return int(concat)

def getTimePlayed(html):
    timeplayed = html.find("span", {"title":"Time played"})
    if timeplayed is None or len(timeplayed.text)<=3:
        return 0
    else:
        timeplayed = timeplayed.text
        output = ""
        lastchar=None
        for char in timeplayed:
            if char != "h":
                output+=char
                if lastchar == "h":
                    return int(output[:-1])
            lastchar = char

def getFinished(html):
    isfinished = html.find("span", {"title":"Story completed"})
    if isfinished is None:
        return False 
    else:
        return True

def getCompleted(html):
    iscompleted = html.find("span", {"title":"Completed including owned DLC"})
    if iscompleted is None:
        return False 
    else:
        return True

