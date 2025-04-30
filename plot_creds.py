# Author: Alison Silldorff
# Date: 3/12/24
# plot_creds.py
# Purpose: analyze credit gender data distilled from analyze_creds.

# %%

import json
import numpy
import requests
import csv
import pandas as pd
from matplotlib import pyplot as plt
import math

# for each tmdbid cast entry of creds_dict_filt, it has the following: [#men, #women, #nb, #missing/other, #total]

file_creds = open("creds_dict_filt_new")
credits = json.load(file_creds)

f_fem_dirs = open("fem_dirs")
fem_dirs = set(json.load(f_fem_dirs))

f_male_dirs = open("male_dirs")
male_dirs = set(json.load(f_male_dirs))


f_oscarnoms = "my_oscarnoms.csv"
# to keep track of which ones we've done
processed_ids = set()

accessed_ids = set()


# first listed actor data by year
y_overall = []
y_bestpic = []
y_bestactor = []
y_bestactress = []
y_bestdir = []
y_bestsupactor = []
y_bestsupactress = []

# films by year where the first actress is a woman
f_y_overall = []
f_y_bestpic = []
f_y_bestactor = []
f_y_bestactress = []
f_y_bestdir = []
f_y_bestsupactor = []
f_y_bestsupactress = []

fem_dirs_count = [0]*3
male_dirs_count = [0]*3

f_fem_dirs_count = [0]*4
f_male_dirs_count = [0]*4

for i in range(96):
    # for these, we'll do a ternary male/female/nb/nodata for who is listed in the top billing spot.
    y_overall.append([0]*3)
    y_bestpic.append([0]*3)
    y_bestactor.append([0]*3)
    y_bestactress.append([0]*3)
    y_bestdir.append([0]*3)
    y_bestsupactor.append([0]*3)
    y_bestsupactress.append([0]*3)

    # so we can have the total women and the total films for each year for these categories.
    f_y_overall.append([0]*4)
    f_y_bestpic.append([0]*4)
    f_y_bestdir.append([0]*4)
    f_y_bestactor.append([0]*4)
    f_y_bestactress.append([0]*4)
    f_y_bestsupactor.append([0]*4)
    f_y_bestsupactress.append([0]*4)

# [overall, bestpic, bestdir, bestactor, bestactress, bestsupactor, bestsupactress]
totals = [0]*7


cast_stats = []
#cast_dist = []
top_billed = []
top_billed_bech = []
for i in range(10):
    cast_stats.append([0]*5)
    top_billed.append([0]*6)
    top_billed_bech.append([0]*6)
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
        ctgry = row[2]
        yr = int(row[1]) - 1929
        if tmdbid not in processed_ids:
            processed_ids.add(tmdbid)
            totals[0]+=1
            for i in range(3):
                y_overall[yr][i] += credits[tmdbid][i]
            for i in range(4):
                print(credits[tmdbid][6][i])
                f_y_overall[yr][i] += credits[tmdbid][6][i]
            if tmdbid in fem_dirs:
                for i in range(3):
                    fem_dirs_count[i]+=credits[tmdbid][i]
                for i in range(4):
                    f_fem_dirs_count[i]+=credits[tmdbid][6][i]
            elif tmdbid in male_dirs:
                for i in range(3):
                    male_dirs_count[i]+=credits[tmdbid][i]
                for i in range(4):
                    f_male_dirs_count[i]+=credits[tmdbid][6][i]
        # [cast #of men, #of women, #nb, #other, #total]
        for i in range(3):
            if ctgry == "Academy Award for Best Picture":
                y_bestpic[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[1]+=1
                    for j in range(4):
                        f_y_bestpic[yr][j] += credits[tmdbid][6][j]
            elif ctgry == "Academy Award for Best Director" or ctgry == "Academy Award for Best Director (Dramatic Picture)" or ctgry == "Academy Award for Best Director (Comedy Picture)":
                y_bestdir[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[2]+=1
                    for j in range(4):
                        f_y_bestdir[yr][j] += credits[tmdbid][6][j]
            elif ctgry == "Academy Award for Best Actor":
                y_bestactor[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[3]+=1
                    for j in range(4):
                        f_y_bestactor[yr][j] += credits[tmdbid][6][j]
            elif ctgry == "Academy Award for Best Actress":
                y_bestactress[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[4]+=1
                    for j in range(4):
                        f_y_bestactress[yr][j] += credits[tmdbid][6][j]
            elif ctgry =="Academy Award for Best Supporting Actor":
                y_bestsupactor[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[5]+=1
                    for j in range(4):
                        f_y_bestsupactor[yr][j] += credits[tmdbid][6][j]
            elif ctgry =="Academy Award for Best Supporting Actress":
                y_bestsupactress[yr][i] += credits[tmdbid][i]
                if i == 0:
                    totals[6]+=1
                    for j in range(4):
                        f_y_bestsupactress[yr][j] += credits[tmdbid][6][j]

print(f_y_bestactor)

labels = 'men', 'women', 'non-binary'
fig, ax = plt.subplots()
ax.set_title('Cast Gender Breakdown of Oscar-Nominated Films')
overall = [0]*3
for i in range(96):
    for j in range(3):
        overall[j]+= y_overall[i][j]
ax.pie(overall, labels=labels, autopct='%1.1f%%')

# %%
# create ternary percentages for noms in each category
p_overall = []
p_bestpic = []
p_bestdir = []
p_bestactor = []
p_bestactress = []
p_bestsupactor = []
p_bestsupactress = []

p_f_overall = []
p_f_bestpic = []
p_f_bestdir = []
p_f_bestactor = []
p_f_bestactress = []
for i in range(96):
    # calculate for overall
    total = sum(y_overall[i])
    print(y_overall[i])
    print(total)
    if total > 0:
        men = float(y_overall[i][0])/total
        women = float(y_overall[i][1])/total
        nb = float(y_overall[i][2])/total
        p_overall.append((men, women, nb))
    else:
        p_overall.append((0, 0, 0))

    # bestpic
    total = sum(y_bestpic[i])
    if total > 0:
        men = float(y_bestpic[i][0])/total
        women = float(y_bestpic[i][1])/total
        nb = float(y_bestpic[i][2])/total
        p_bestpic.append((men, women, nb))
    else:
        p_bestpic.append((0, 0, 0))

    #bestdir
    total = sum(y_bestdir[i])
    if total > 0:
        men = float(y_bestdir[i][0])/total
        women = float(y_bestdir[i][1])/total
        nb = float(y_bestdir[i][2])/total
        p_bestdir.append((men, women, nb))
    else:
        p_bestdir.append((0, 0, 0))

    #bestactor
    total = sum(y_bestactor[i])
    if total > 0:
        men = float(y_bestactor[i][0])/total
        women = float(y_bestactor[i][1])/total
        nb = float(y_bestactor[i][2])/total
        p_bestactor.append((men, women, nb))
    else:
        p_bestactor.append((0, 0, 0))

    #bestactress
    total = sum(y_bestactress[i])
    if total > 0:
        men = float(y_bestactress[i][0])/total
        women = float(y_bestactress[i][1])/total
        nb = float(y_bestactress[i][2])/total
        p_bestactress.append((men, women, nb))
    else:
        p_bestactress.append((0, 0, 0))

    #bestsupactor
    total = sum(y_bestsupactor[i])
    if total > 0:
        men = float(y_bestsupactor[i][0])/total
        women = float(y_bestsupactor[i][1])/total
        nb = float(y_bestsupactor[i][2])/total
        p_bestsupactor.append((men, women, nb))
    else:
        p_bestsupactor.append((0, 0, 0))

    #bestsupactress
    total = sum(y_bestsupactress[i])
    if total > 0:
        men = float(y_bestsupactress[i][0])/total
        women = float(y_bestsupactress[i][1])/total
        nb = float(y_bestsupactress[i][2])/total
        p_bestsupactress.append((men, women, nb))
    else:
        p_bestsupactress.append((0, 0, 0))
    
    # f_y_overall
    # f_y_bestpic
    # f_y_bestdir
    total = sum(f_y_overall[i])
    if total > 0:
        men = float(f_y_overall[i][0])/total
        women = float(f_y_overall[i][1])/total
        nb = float(f_y_overall[i][2])/total
        nodata = float(f_y_overall[i][3])/total
        p_f_overall.append((men, women, nb, nodata))
    else:
        p_f_overall.append([0]*4)

    total = sum(f_y_bestpic[i])
    if total > 0:
        men = float(f_y_bestpic[i][0])/total
        women = float(f_y_bestpic[i][1])/total
        nb = float(f_y_bestpic[i][2])/total
        nodata = float(f_y_bestpic[i][3])/total
        p_f_bestpic.append((men, women, nb, nodata))
    else:
        p_f_bestpic.append([0]*4)
    
    total = sum(f_y_bestdir[i])
    if total > 0:
        men = float(f_y_bestdir[i][0])/total
        women = float(f_y_bestdir[i][1])/total
        nb = float(f_y_bestdir[i][2])/total
        nodata = float(f_y_bestdir[i][3])/total
        p_f_bestdir.append((men, women, nb, nodata))
    else:
        p_f_bestdir.append([0]*4)
    
    total = sum(f_y_bestactor[i])
    if total > 0:
        men = float(f_y_bestactor[i][0])/total
        women = float(f_y_bestactor[i][1])/total
        nb = float(f_y_bestactor[i][2])/total
        nodata = float(f_y_bestactor[i][3])/total
        p_f_bestactor.append((men, women, nb, nodata))
    else:
        p_f_bestactor.append([0]*4)

    total = sum(f_y_bestactress[i])
    if total > 0:
        men = float(f_y_bestactress[i][0])/total
        women = float(f_y_bestactress[i][1])/total
        nb = float(f_y_bestactress[i][2])/total
        nodata = float(f_y_bestactress[i][3])/total
        p_f_bestactress.append((men, women, nb, nodata))
    else:
        p_f_bestactress.append([0]*4)



# %%
# Cast gender breakdown by percent
tr_p_overall = numpy.transpose(p_overall)
plt.plot(tr_p_overall[1], label='women', color='orange')
plt.plot(tr_p_overall[0], label='men', color='blue')
plt.plot(tr_p_overall[2], label='non-binary', color='green')
plt.title('Percent by Year of Cast Gender Breakdown in Oscar-nominated Films')
years = numpy.arange(1929, 2024, step=10)
plt.xticks(numpy.arange(0, 100, step=10), labels=years)
plt.yticks(numpy.arange(0, 1.1, step=0.1), labels=numpy.arange(0, 110, step=10))
plt.ylabel('percent')
leg = plt.legend(loc='upper center')

# %%
# look at female protagonists over time
# line graph

tr_p_f_bestpic = numpy.transpose(p_f_bestactress)
# mean from 1929-1970
#print(numpy.mean(tr_p_f_bestpic[1][0:41]))
# mean from 1970-2010
#print(numpy.mean(tr_p_f_bestpic[1][41:82]))
#print(tr_p_f_overall)
plt.plot(tr_p_f_bestpic[1], label='women',color='orange')
#plt.plot(tr_p_f_overall[0], label='men',color='blue')
plt.title('Percent by Year of Best Actress Nominees with a Woman First in Cast Ordering')
years = numpy.arange(1929, 2024, step=10)
plt.xticks(numpy.arange(0, 100, step=10), labels=years)
plt.yticks(numpy.arange(0, 1.1, step=0.1), labels=numpy.arange(0, 110, step=10))
plt.ylabel('percent')
leg = plt.legend(loc='upper center')

# %%
# look at female protagonist as a percent
# pie chart
t_bestpic = [0]*4
for i in range(96):
    for j in range(4):
        t_bestpic[j]+=f_y_bestsupactor[i][j]
t_pie = [t_bestpic[0], t_bestpic[2], t_bestpic[1], t_bestpic[3]]
#t_overall = numpy.transpose(f_y_overall)
#f_pie = [sum(t_overall[0]), totals[0]-sum(t_overall[0])]
labels = 'Man', 'non-binary','woman', 'no data'
fig, ax = plt.subplots()
ax.set_title('Gender Breakdown of the First Listed Actor in Best Supporting Actor Nominees')
ax.pie(t_pie, labels=labels, autopct='%1.1f%%', colors=['cornflowerblue','salmon', 'orange','red'])

#%%
# cast breakdown for m and f dirs
labels = 'men', 'women', 'non-binary'
fig, ax = plt.subplots()
ax.set_title('Cast Gender Breakdown of Oscar-Nominated Films Directed by Women')
ax.pie(fem_dirs_count, labels=labels, autopct='%1.1f%%')
#%%
fig, ax = plt.subplots()
ax.set_title('Cast Gender Breakdown of Oscar-Nominated Films Directed by Men')
ax.pie(male_dirs_count, labels=labels, autopct='%1.1f%%')

#%%
#first actor breakdown for m and f dirs
labels = 'men','non-binary', 'women',  'no data'
fig, ax = plt.subplots()
ax.set_title('Gender Breakdown of the First Listed Actor in Oscar-Nominated Films Directed by Men')
f_pie = [f_male_dirs_count[0], f_male_dirs_count[2], f_male_dirs_count[1], f_male_dirs_count[3]]
ax.pie(f_pie, labels=labels, autopct='%1.1f%%', colors=['cornflowerblue','salmon', 'orange','red'])

#%%

# first let's go year by year and show gender breakdown of each decade.
# just use unique values (don't count a movie nominated for two awards twice. count it once)
cast_stats_per = []
#cast_dist_per = []
top_billed_per = [] # % of films with a woman in the ith billing spot.
billed_bech_per = [] # % of films with a woman in the ith billing spot that pass the Bechdel test

# assumption that missing entries, if filled out, would maintain the ratio between men/women/nb
#therefore we omit that in our percentages calculation.
for entry in cast_stats:
    total = entry[0]+entry[1]+entry[2]
    cast_stats_per.append([round((100*entry[0]/total), 2), round((100*entry[1]/total), 2), round((100*entry[2]/total), 2)])

curr_dec = 0
for entry in top_billed:
    curr = []
    for i in range(6):
        # percent of total films in the decade that have a woman in the ith spot.
        curr.append(round(100*(entry[i]/dec_totals[curr_dec]), 2))
    top_billed_per.append(curr)
    curr_dec += 1

curr_dec = 0
for entry in top_billed_bech:
    curr = []
    for i in range(6):
        curr.append(round(100*(entry[i]/top_billed[curr_dec][i]), 2))
    billed_bech_per.append(curr)
print(top_billed_per)
print(billed_bech_per)

#for entry in cast_dist:
    #total = sum(entry)
    #curr = []
    #for i in range(10):
        #curr.append(round(100*(entry[i]/total), 2))
    #cast_dist_per.append(curr)
#for entry in cast_dist_per:
    #print(entry)


#for entry in cast_stats_per:
    #print(entry)

# %%


#plot top_billed_per

dec_labels = ["1929-1939", "1940s", "1950s", "1960s", "1970s", "1980s", "1990s", "2000s", "2010s", "2020s"]


x = numpy.arange(6)  # the label locations
width = 0.4  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

#plt.rcParams['font.size'] = 8.2

rects = ax.bar(x, top_billed_per[9], width)
ax.bar_label(rects, padding=10)
creds_x_labels = ["1st", "2nd", "3rd", "4th", "5th", "no women in top 5"]

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Percent of total nominated films')
ax.set_title('Percent of Nominated Films (2020s) with a Woman in the ith Billing Spot')
ax.set_xticks(x, creds_x_labels)
ax.set_ylim(0, 100)

plt.show()



# %%


# %%
cast_stats_per = numpy.transpose(cast_stats_per)
#print(cast_stats_per)
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