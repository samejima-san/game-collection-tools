#!/usr/bin/env python3
import slibexp
import xlibexp
import plibexp
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
# Replace with your Steam API key and Steam ID
API_KEY = os.getenv("API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

base_dir = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(base_dir, "/.logs", "updatequery.txt")

# Connect to your database
conn = psycopg2.connect(
    dbname=os.getenv("DBNAME"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    host="localhost",  # Change if using a remote server
    port="5432"
)


def autoupdatedb():
    cur = conn.cursor()
    slibexp.update_gametime()
    with open('.updatequery', "r") as f:
        steam_string = f.read()
    if(len(steam_string)==0):
        print("steam, nothing to add.")
    xlibexp.update_gametime()
    with open('.xbox_query', "r") as f:
        xbox_string = f.read()
    if(len(xbox_string)==0):
        print("xbox, nothing to add.")
    plibexp.update_gametime()
    with open('.playstation_query', "r") as f:
        playstation_string = f.read()
    if(len(playstation_string)==0):
        print("playstation, nothing to add.")
    cur.execute(xbox_string)
    cur.execute(steam_string)
    cur.execute(playstation_string)
    conn.commit()
    cur.close()
    conn.close()
    print("updated database")
    return


if __name__ == "__main__":
    autoupdatedb()
