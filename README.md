# Princeton University CS Junior Independent Research-- Quantifying Female Representation at the Oscars
This project aims to quantify and analyze female representation at the Oscars, both in terms of the makeup of nominees and the quality of representation within Oscar-nominated films. Using the Selenium library in Python, I scraped data on Oscar-nominated films from TMDB. I also used the API on bechdeltest.com to collect Bechdel Test scores for Oscar-nominated films. This research culminated in a 25-page research paper.    

Advised by Professor Brian Kernighan.

## Abstract
This project analyzes Academy Award nomination data to analyze female representation in Oscar-nominated films since the start of the awards in 1929. Female representation is measured using Bechdel Test scores, gender breakdown of the cast, gender breakdown of above the line crew positions, and gender breakdown of the first-listed actor for a film. The results reinforce that women have been historically underrepresented in Oscar-nominated films. In particular, women comprise about half as much of the casts of Oscar-nominated films as men, and this ratio has changed very little over each year of the Academy Awards. It is also found that films directed by women have better female representation (according to these metrics) than films directed by men.

## Files
**Junior Paper FINAL.pdf** Final written paper  
**analyze_creds.py** process credit gender data collected from parse_credits.py  
**credits.py** scrape credits data from TMDB  
**parse_credits.py** process credits scraped from TMDB  
**plot_creds.py** analyze credit gender data distilled from analyze_creds  
**plot_crew_creds.py** analyze credit gender data distilled from parse_credits.py  
**plotting.py** plot Bechdel Test data
