#!/usr/bin/env python3
import slibexp
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()
# Replace with your Steam API key and Steam ID
API_KEY = os.getenv("API_KEY")
STEAM_ID = os.getenv("STEAM_ID")

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
    with open("updatequery.txt", "r") as f:
        query_string = f.read()
    if(len(query_string)==0):
        print("nothing to add to Database")
        cur.close()
        conn.close()
        return
    cur.execute(query_string)
    conn.commit()
    cur.close()
    conn.close()
    print("updated database")
    return


if __name__ == "__main__":
    autoupdatedb()
