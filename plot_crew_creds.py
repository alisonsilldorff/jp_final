# Author: Alison Silldorff
# Date: 3/12/24
# plot_crew_creds.py
# Purpose: analyze credit gender data distilled from parse_credits.py

# %%

import json
import numpy
import requests
import csv
import pandas as pd
from matplotlib import pyplot as plt
import math

file_creds = open("crew_creds_dict")
credits = json.load(file_creds)

f_fem_dirs = open("fem_dirs")
fem_dirs = set(json.load(f_fem_dirs))

f_male_dirs = open("male_dirs")
male_dirs = set(json.load(f_male_dirs))


f_oscarnoms = "my_oscarnoms.csv"
# to keep track of which ones we've done
processed_ids = set()

def get_decade(year):
    return int((year -1929) / 10)


dec_totals = [0]*10 #total number of unique films per decade. for use later.
atl_totals = [0]*4
btl_totals = [0]*4

atl_stats = []
btl_stats = []
atl_fem_dirs = []
atl_male_dirs = []
#cast_dist = []
#top_billed = []
#top_billed_bech = []
for i in range(96):
    atl_stats.append([0]*4)
    btl_stats.append([0]*4)
    atl_fem_dirs.append([0]*4)
    atl_male_dirs.append([0]*4)
    #top_billed.append([0]*6)
    #top_billed_bech.append([0]*6)
    #cast_dist.append([0]*10) # for each decade, one entry for each ten percent

# for every five percent, and for every decade, we want to sum the number of women whose listing falls in that ten percent
# for each entry


with open(f_oscarnoms, 'r', encoding="utf-8") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        # first row. don't use it.
        if row[0] == "awardEditionLabel":
            continue
        tmdbid = row[9]
        if tmdbid not in processed_ids:
            processed_ids.add(tmdbid)
            # [cast #of men, #of women, #nb, #other, #total]

            # year
            i = int(row[1]) - 1929
            if tmdbid in fem_dirs:
                atl_fem_dirs[i][0] += credits[tmdbid][0][0]
                atl_fem_dirs[i][1] += credits[tmdbid][0][1]
                atl_fem_dirs[i][2] += credits[tmdbid][0][2]
                atl_fem_dirs[i][3] += credits[tmdbid][0][3]
            elif tmdbid in male_dirs:
                atl_male_dirs[i][0] += credits[tmdbid][0][0]
                atl_male_dirs[i][1] += credits[tmdbid][0][1]
                atl_male_dirs[i][2] += credits[tmdbid][0][2]
                atl_male_dirs[i][3] += credits[tmdbid][0][3]

            
            atl_stats[i][0] += credits[tmdbid][0][0]
            atl_stats[i][1] += credits[tmdbid][0][1]
            atl_stats[i][2] += credits[tmdbid][0][2]
            atl_stats[i][3] += credits[tmdbid][0][3]

            btl_stats[i][0] += credits[tmdbid][1][0]
            btl_stats[i][1] += credits[tmdbid][1][1]
            btl_stats[i][2] += credits[tmdbid][1][2]
            btl_stats[i][3] += credits[tmdbid][1][3]

            crew_size = credits[tmdbid][2]
            bech = row[10]
            #for entry in credits[tmdbid][5]:
                # in a given decade, in the percentile of the entry in the cast list, increment by 1.
                #print(get_percentile(entry, cast_size))
                #print(entry, cast_size)
                #cast_dist[dec][get_percentile(entry, cast_size)] += 1

#get totals
for i in range(10):
    for j in range(4):
        atl_totals[j] += atl_stats[i][j]
        btl_totals[j] += btl_stats[i][j]

#print(top_billed)

print(atl_fem_dirs)


# first let's go year by year and show gender breakdown of each decade.
# just use unique values (don't count a movie nominated for two awards twice. count it once)
atl_stats_per = []
btl_stats_per = []
atl_male_per = []
atl_fem_per = []
#cast_dist_per = []
top_billed_per = [] # % of films with a woman in the ith billing spot.
billed_bech_per = [] # % of films with a woman in the ith billing spot that pass the Bechdel test

# assumption that missing entries, if filled out, would maintain the ratio between men/women/nb
#therefore we omit that in our percentages calculation.
for entry in atl_stats:
    total = entry[0]+entry[1]+entry[2]
    atl_stats_per.append([round((100*entry[0]/total), 2), round((100*entry[1]/total), 2), round((100*entry[2]/total), 2)])
for entry in btl_stats:
    total = entry[0]+entry[1]+entry[2]
    btl_stats_per.append([round((100*entry[0]/total), 2), round((100*entry[1]/total), 2), round((100*entry[2]/total), 2)])
for entry in atl_fem_dirs:
    total = entry[0]+entry[1]+entry[2]
    if total == 0:
        atl_fem_per.append((0,0,0))
    else:
        atl_fem_per.append([round((100*entry[0]/total), 2), round((100*entry[1]/total), 2), round((100*entry[2]/total), 2)])
for entry in atl_male_dirs:
    total = entry[0]+entry[1]+entry[2]
    atl_male_per.append([round((100*entry[0]/total), 2), round((100*entry[1]/total), 2), round((100*entry[2]/total), 2)])


print(atl_stats_per)



# %%


dec_labels = ["1929-1939", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]
years = numpy.arange(1929, 2025, step=10)

trpatl = numpy.transpose(atl_stats_per)
trpbtl = numpy.transpose(btl_stats_per)



#plot the pass/fails/none for noms
#plt.plot(trpncount[0], label='fails')
plt.plot(trpatl[1], label='Women',color='orange')
print(numpy.argmax(trpatl[1]))
# Percent by Year of ATL Crew Positions Held by Women on Oscar-Nominated Films
plt.title('Percent by Year of ATL Positions Held by Women on Oscar-Nominated Films')
#plt.xlabel(years)
plt.ylabel("Percent")
#plt.plot(trpncount[2], label='no data')
plt.xticks(numpy.arange(0, 100, step=10), labels=years)
plt.ylim(0, 100)
plt.yticks(numpy.arange(0, 100, step=10), labels=numpy.arange(0, 100, step=10))
leg = plt.legend(loc='upper center')

plt.show()



# %%
labels = 'Men', 'Women', 'Non-Binary'
atl_pie = [sum(trpatl[0]), sum(trpatl[1]), sum(trpatl[2])]
fig, ax = plt.subplots()
ax.set_title('Gender Breakdown of ATL Positions in Oscar-Nominated Films')
ax.pie(atl_pie, labels=labels, autopct='%1.1f%%', colors=['cornflowerblue','orange','salmon'])

# %%
# count movies with female directors and male directors' atl crews
tr_atl_fem_dirs = numpy.transpose(atl_fem_per)
tr_atl_male_dirs = numpy.transpose(atl_male_per)

plt.plot(tr_atl_male_dirs[1], label='Women',color='orange')
print(numpy.argmax(trpatl[1]))
# Percent by Year of ATL Crew Positions Held by Women on Oscar-Nominated Films
plt.title('Percent by Year of ATL Positions Held by Women on Oscar-Nominated Films (fem dir)')
plt.ylabel("Percent")
plt.xticks(numpy.arange(0, 100, step=10), labels=years)
plt.ylim(0, 100)
plt.yticks(numpy.arange(0, 100, step=10), labels=numpy.arange(0, 100, step=10))
leg = plt.legend(loc='upper center')

plt.show()


# %%
dec_labels = ["1929-1939", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]


x = numpy.arange(10)  # the label locations
#print(x)
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')
fig.set_figwidth(200)
plt.rcParams['font.size'] = 8.2

#for attribute, measurement in penguin_means.items():
#10 decades
for i in range(3):
    offset = width * multiplier
    rects = ax.bar(x + offset, cast_stats_per[i], width)
    ax.bar_label(rects, padding=10)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percent of cast')
ax.set_title('Gender Breakdown of Casts of Oscar-Nominated Films')
ax.set_xticks(x + width, dec_labels)
ax.legend(["male", "female", "non-binary"], loc='upper left', ncols=3)
ax.set_ylim(0, 100)

plt.show()

# %%



file_creds.close()