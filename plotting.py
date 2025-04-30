# Author: Alison Silldorff
# Date: 3/12/24
# plotting.py
# Purpose: plot Bechdel Test data for JP

# %%
# process the data

import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import math
import csv
import json

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True  

f_fem_dirs = open("fem_dirs")
fem_dirs = set(json.load(f_fem_dirs))

f_male_dirs = open("male_dirs")
male_dirs = set(json.load(f_male_dirs))

accessed_ids = set()

# bechdel test data for all data for each category. not separated by year.
overall = [0]*5
bestpic = [0]*5
bestactor = [0]*5
bestactress = [0]*5
bestdir = [0]*5
bestsupactor = [0]*5
bestsupactress = [0]*5

# bechdel test data by year
y_overall = []
y_bestpic = []
y_bestactor = []
y_bestactress = []
y_bestdir = []
y_bestsupactor = []
y_bestsupactress = []

fem_dirs_bech = [0]*5
male_dirs_bech = [0]*5

for i in range(96):
    # for these, we'll just do a ternary pass/fail/nodata
    y_overall.append([0]*3)
    y_bestpic.append([0]*3)
    y_bestactor.append([0]*3)
    y_bestactress.append([0]*3)
    y_bestdir.append([0]*3)
    y_bestsupactor.append([0]*3)
    y_bestsupactress.append([0]*3)

f_oscarnoms = "my_oscarnoms.csv"
with open(f_oscarnoms, 'r', encoding="utf-8") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        # first row. don't use it.
        if row[0] == "awardEditionLabel":
            continue

        bech = row[10]
        ter_bech = 0 # ternary bechdel score: 0=fail 1=pass 2=nodata
        ctgry = row[2]
        yr = int(row[1]) - 1929
        if bech == '':
            bech = 4
            ter_bech = 2
        else:
            bech = int(bech)
        
        if bech == 3:
            ter_bech = 1

        if row[8] not in accessed_ids:
            accessed_ids.add(row[8])
            overall[bech] += 1
            y_overall[yr][ter_bech] += 1
            # process the bechdel test scores for male and female directors
            tmdbid = row[9]
            if tmdbid in fem_dirs:
                fem_dirs_bech[bech]+=1
            elif tmdbid in male_dirs:
                male_dirs_bech[bech]+=1

        if ctgry == "Academy Award for Best Picture":
            bestpic[bech] +=1
            y_bestpic[yr][ter_bech] += 1
        elif ctgry == "Academy Award for Best Director" or ctgry == "Academy Award for Best Director (Dramatic Picture)" or ctgry == "Academy Award for Best Director (Comedy Picture)":
            bestdir[bech]+=1
            y_bestdir[yr][ter_bech] += 1
        elif ctgry == "Academy Award for Best Actor":
            bestactor[bech]+=1
            y_bestactor[yr][ter_bech] += 1
        elif ctgry == "Academy Award for Best Actress":
            bestactress[bech]+=1
            y_bestactress[yr][ter_bech] += 1
        elif ctgry =="Academy Award for Best Supporting Actor":
            bestsupactor[bech]+=1
            y_bestsupactor[yr][ter_bech] += 1
        elif ctgry =="Academy Award for Best Supporting Actress":
            bestsupactress[bech]+=1
            y_bestsupactress[yr][ter_bech] += 1




# %%
# make a pie chart for a specific category
labels = '0', '1', '2', '3', 'Not rated'
fig, ax = plt.subplots()
ax.set_title('Bechdel Test Scores of Oscar-Nominated Films')
ax.pie(overall, labels=labels, autopct='%1.1f%%', colors=['darkred', 'firebrick', 'indianred', 'seagreen', 'gray'])


# %%
# pie chart (old version bc now I changed the way the arrays are structured)

#fig, (ax1, ax2) = plt.subplots(1, 2)
#fig.suptitle('Bechdel Test scores of Best Picture nominees and winners')
#ax1.set_title('Nominees')
#ax2.set_title('Winners')
#ax1.pie(ncount, labels=labels, autopct='%1.1f%%', colors=['darkred', 'firebrick', 'indianred', 'seagreen', 'gray'])
#ax2.pie(wcount, labels=labels, autopct='%1.1f%%', colors=['darkred', 'firebrick', 'indianred', 'seagreen', 'gray'])

#print("Contents in csv file:", df)
#plt.plot(df.Name, df.Marks)
#plt.show()


# %%
# create ternary percentages for noms in each category
p_overall = []
p_bestpic = []
p_bestdir = []
p_bestactor = []
p_bestactress = []
p_bestsupactor = []
p_bestsupactress = []
for i in range(96):
    # calculate for overall
    total = sum(y_overall[i])
    if total > 0:
        fails = float(y_overall[i][0])/total
        passes = float(y_overall[i][1])/total
        nodata = float(y_overall[i][2])/total
        p_overall.append((fails, passes, nodata))
    else:
        p_overall.append((0, 0, 0))

    # bestpic
    total = sum(y_bestpic[i])
    if total > 0:
        fails = float(y_bestpic[i][0])/total
        passes = float(y_bestpic[i][1])/total
        nodata = float(y_bestpic[i][2])/total
        p_bestpic.append((fails, passes, nodata))
    else:
        p_bestpic.append((0, 0, 0))

    #bestdir
    total = sum(y_bestdir[i])
    if total > 0:
        fails = float(y_bestdir[i][0])/total
        passes = float(y_bestdir[i][1])/total
        nodata = float(y_bestdir[i][2])/total
        p_bestdir.append((fails, passes, nodata))
    else:
        p_bestdir.append((0, 0, 0))

    #bestactor
    total = sum(y_bestactor[i])
    if total > 0:
        fails = float(y_bestactor[i][0])/total
        passes = float(y_bestactor[i][1])/total
        nodata = float(y_bestactor[i][2])/total
        p_bestactor.append((fails, passes, nodata))
    else:
        p_bestactor.append((0, 0, 0))

    #bestactress
    total = sum(y_bestactress[i])
    if total > 0:
        fails = float(y_bestactress[i][0])/total
        passes = float(y_bestactress[i][1])/total
        nodata = float(y_bestactress[i][2])/total
        p_bestactress.append((fails, passes, nodata))
    else:
        p_bestactress.append((0, 0, 0))

    #bestsupactor
    total = sum(y_bestsupactor[i])
    if total > 0:
        fails = float(y_bestsupactor[i][0])/total
        passes = float(y_bestsupactor[i][1])/total
        nodata = float(y_bestsupactor[i][2])/total
        p_bestsupactor.append((fails, passes, nodata))
    else:
        p_bestsupactor.append((0, 0, 0))

    #bestsupactress
    total = sum(y_bestsupactress[i])
    if total > 0:
        fails = float(y_bestsupactress[i][0])/total
        passes = float(y_bestsupactress[i][1])/total
        nodata = float(y_bestsupactress[i][2])/total
        p_bestsupactress.append((fails, passes, nodata))
    else:
        p_bestsupactress.append((0, 0, 0))

print(p_overall)



# %%
tr_p_overall = np.transpose(p_overall)
#plot the pass/fails/none for noms
plt.plot(tr_p_overall[1], label='passes', color='lime')
plt.plot(tr_p_overall[2], label='no data', color='slategrey')
plt.title('Percentage of Oscar-nominated films that pass the Bechdel Test by year')
#plt.xlabel(years)
#plt.plot(trpncount[2], label='no data')
years = np.arange(1929, 2024, step=10)
plt.xticks(np.arange(0, 100, step=10), labels=years)
plt.yticks(np.arange(0, 1.1, step=0.1), labels=np.arange(0, 110, step=10))
leg = plt.legend(loc='upper center')

# %%
# look at female versus male directors' bechdel test scores
print(fem_dirs_bech)
labels = '0', '1', '2', '3', 'Not rated'
fig, ax = plt.subplots()
ax.set_title('Bechdel Test Scores of Oscar-Nominated Films Directed by a Woman')
ax.pie(fem_dirs_bech, labels=labels, autopct='%1.1f%%', colors=['darkred', 'firebrick', 'indianred', 'seagreen', 'gray'])

print(male_dirs_bech)
labels = '0', '1', '2', '3', 'Not rated'
fig, ax = plt.subplots()
ax.set_title('Bechdel Test Scores of Oscar-Nominated Films Directed by a Man')
ax.pie(male_dirs_bech, labels=labels, autopct='%1.1f%%', colors=['darkred', 'firebrick', 'indianred', 'seagreen', 'gray'])


# %%
