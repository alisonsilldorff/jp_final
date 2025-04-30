# Author: Alison Silldorff
# Date: 3/12/24
# parse_credits.py
# Purpose: process credits scraped from TMDB

import json

CAST_CUTOFF = 35
#CREW_CUTOFF = 20

# above the line positions
atl = set(["Co-Director", "Co-Executive Producer", 
          "Co-Producer", "Co-Writer", "Director", 
          "Director of Photography", "Executive Producer", 
          "Producer", "Screenplay", "Screenstory"])
print(type("casting" not in atl))

fem_dir = set()
male_dir = set()

file = open("creds")
credits = json.load(file)

# tmdbid: [numcastmen, numcastwomen, numcastother, numcastblank, numcasttotal, womencastindices]
cred_dict = {}

# tmdbid : [[atl gender breakdown], [btl gender breakdown], totalnumcrew]
cred_dict_crew = {}

# iterate through each film in the dictionary!
for id, creds in credits.items():
    f = 0 #female
    m = 0 #male
    nb = 0 #non-binary
    o = 0 #not specified/other/blank
    i = 1 #index
    fs = [] # the indices of all women
    first = [0]*4
    # genders: 0="not set/notspecified" , 1=f, 2=m, 3=nb
    if creds[0] is None:
        continue
    for entry in creds[0]:
        if i > CAST_CUTOFF:
            break
        gender = entry["gender"]
        if i == 1:
            if gender == 1:
                first[1]=1
            elif gender == 2:
                first[0] = 1
            elif gender == 3:
                first[2]=1
            else:
                first[3]=1
        if gender==1:
            f += 1
            fs.append(i)
        elif gender==2:
            m += 1
        elif gender==3:
            nb +=1
        else:
            o += 1
        i += 1
    stats = [m, f, nb, o, i-1, fs, first]    
    cred_dict.update({id:stats})
    
    af = 0 # above the line, female
    am = 0 # above the line, male
    anb = 0
    ao = 0
    bf = 0 # below the line, female
    bm = 0
    bnb = 0
    bo = 0
    i = 1 # count
    if creds[1] is None:
        continue
    for entry in creds[1]:
        # 1 = atl, 0 = btl
        line = entry["job"] in atl
        gender = entry["gender"]
        if entry["job"]=="Director" or entry["job"]=="Co-Director":
            if gender == 1:
                fem_dir.add(id)
            elif gender == 2:
                male_dir.add(id)
        if gender==1:
            if line:
                af += 1
            else:
                bf += 1  
        elif gender==2:
            if line:
                am += 1
            else:
                bm += 1
        elif gender==3:
            if line:
                anb +=1
            else:
                bnb +=1
        else:
            if line:
                ao += 1
            else:
                bo += 1
        i += 1
    crew_stats = [[am, af, anb, ao], [bm, bf, bnb, bo], i-1]
    cred_dict_crew.update({id:crew_stats})
    
    
#print(cred_dict)
f_out = "creds_dict_filt_new"
with open(f_out, 'w', encoding="utf-8") as f:
    f.write(json.dumps(cred_dict))

f_out_1 = "crew_creds_dict"
with open(f_out_1, 'w', encoding="utf-8") as f:
    f.write(json.dumps(cred_dict_crew))

f_out_2 = "fem_dirs"
f_out_3 = "male_dirs"
with open(f_out_2, 'w', encoding="utf-8") as f:
    f.write(json.dumps(list(fem_dir)))
with open(f_out_3, 'w', encoding="utf-8") as f:
    f.write(json.dumps(list(male_dir)))



file.close()
    