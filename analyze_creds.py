# Author: Alison Silldorff
# Date: 3/12/24
# analyze_creds.py
# Purpose: process credit gender data collected from parse_credits.py

import json
import numpy

file = open("creds_dict_filt")
credits = json.load(file)



cast_size = []
cast_nodata = []
cast_nodata_per = [] #percentage of nodata for cast. nodata / size
crew_size = []
crew_nodata = []
crew_nodata_per = [] #percentage of nodata for crew. nodata / size
castlots_missing = []
castfew_missing = []
crewlots_missing =[]
crewfew_missing = []
for id, creds in credits.items():
    # add cast size
    cast_size.append(creds[4])
    cast_nodata.append(creds[3])
    if creds[4] > 35:
        castlots_missing.append(creds[3])
    else:
        castfew_missing.append(creds[3])
    cast_nodata_per.append(creds[3]/creds[4])
    # add crew size
    crew_size.append(creds[10])
    crew_size.append(creds[9])
    if creds[10] > 20:
        crewlots_missing.append(creds[9])
    else:
        crewfew_missing.append(creds[9])
    crew_nodata_per.append(creds[9]/creds[10])



#print(numpy.percentile(cast_size, 75))
#print(numpy.percentile(crew_size, 75))

print(numpy.mean(cast_size))
print(numpy.median(cast_size))

print(numpy.mean(cast_nodata_per))
print(numpy.median(cast_nodata_per))

print(numpy.mean(crew_size))
print(numpy.median(crew_size))

print(numpy.mean(crew_nodata_per))
print(numpy.median(crew_nodata_per))
#print(castlots_missing)
#print(crewlots_missing)
#print(numpy.mean(castlots_missing))
#print(numpy.mean(castfew_missing))
#print(numpy.mean(crewlots_missing))
#print(numpy.mean(crewfew_missing))
file.close()