# Author: Alison Silldorff
# Date: 3/12/24
# credits.py
# Purpose: scrape credits data from TMDB

import csv
import requests
import json
import pandas as pd

key = open("C:\\Users\\12676\\tmdb_info", 'r').read()

f_oscarnoms = "my_oscarnoms.csv"
credits = {}

with open(f_oscarnoms, 'r', encoding="utf-8") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        tmdbid = row[9]
        if tmdbid not in credits:
            # scrape, then
            response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdbid}/credits?api_key={key}")
            res = response.json()
            credits.update({tmdbid:[res.get("cast"), res.get("crew")]})


# let's try to get credits for one movie. Let's use Barbie
# https://api.themoviedb.org/3/movie/346698?api_key={key}&append_to_response=credits
#tmdbid = "346698"
#response = requests.get(f"https://api.themoviedb.org/3/movie/{tmdbid}/credits?api_key={key}")
#res = response.json()
#print(type(res))
#print(res.get("cast"))

f_out = "creds"
with open(f_out, 'w', encoding="utf-8") as f:
    f.write(json.dumps(credits))
