# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

base_site = "https://editorial.rottentomatoes.com/guide/140-essential-action-movies-to-watch-now/2/"

response = requests.get(base_site)
response.status_code

html = response.content
soup = BeautifulSoup(html, 'lxml')

with open('Rotten_tomatoes_page_2_LXML_Parser.html', 'wb') as file:
    file.write(soup.prettify('utf-8'))

divs = soup.find_all("div", {"class": "col-sm-18 col-full-xs countdown-item-content"})
headings = [div.find("h2") for div in divs]

titles = [heading.find('a').string for heading in headings]

years = [heading.find('span', class_ = 'start-year').string for heading in headings]

years_cleaned = [year.strip('()') for year in years]

years_int = [int(year) for year in years_cleaned]

scores = [heading.find('span', class_= 'tMeterScore').string for heading in headings]
score_vals = [score.strip('%') for score in scores]
score_int_vals = [int(score) for score in score_vals]

#score_int_vals[:5]

consensus = [div.find(class_ ="info critics-consensus").text for div in divs]
#consensus[:5]

consensus_clean = [con.strip('Critics Consensus: ') for con in consensus]
#consensus_clean[:5]

director_list = [div.find(class_ ="info director").contents[3].text for div in divs]
#director_list[:10]

cast_list = [div.find('div', {'class': "info cast"}).find_all('a') for div in divs]
cast = [", ".join([link.string for link in c]) for c in cast_list]
#cast[:5]

adj_score = [float(div.find("div", {"class": "info countdown-adjusted-score"}).contents[1].strip('% ')) for div in divs]
#adj_score[0]

synopsis = [div.find('div',{'class' : "info synopsis"}).contents[1].strip("' ") for div in divs]
synopsis[:5]

movies_df = pd.DataFrame()

movies_df["Movie Title"] = titles
movies_df["Year"] = years_int
movies_df["Score"] = score_int_vals
movies_df["Adjusted Score"] = adj_score  
movies_df["Director"] = director_list
movies_df["Synopsis"] = synopsis    
movies_df["Cast"] = cast
movies_df["Consensus"] = consensus_clean

movies_df.to_excel("rotten_tomatoes_140action.xlsx", index = False, header = True)
movies_df.to_csv("rotten_tomatoes_140action.csv", index = False, header = True)
