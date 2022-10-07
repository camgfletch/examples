#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup

master_df = pd.DataFrame()

urls = ['https://www.basketball-reference.com/boxscores/202110190LAL.html', 
        'https://www.basketball-reference.com/boxscores/202110190MIL.html']

for url in urls:
    tables = pd.read_html(url)
    away_basic = tables[0]
    away_adv = tables[7]
    home_basic = tables[8]
    home_adv = tables[15]
    
    away_basic_df = away_basic_df.droplevel(level=0, axis=1)
    away_adv_df = away_adv_df.droplevel(level=0, axis=1)
    home_basic_df = home_basic_df.droplevel(level=0, axis=1)
    home_adv_df = home_adv_df.droplevel(level=0, axis=1)
    
    away_df = pd.merge(away_basic_df,away_adv_df,on=['Starters', 'MP'])
    home_df = pd.merge(home_basic_df,home_adv_df,on=['Starters', 'MP'])
    
    away_df = away_df[away_df['Starters'].str.contains('Reserves')==False]
    away_df = away_df.rename(columns={'Starters': "Players"}, errors="raise")
    
    home_df = home_df[home_df['Starters'].str.contains('Reserves')==False]
    home_df = home_df.rename(columns={'Starters': "Players"}, errors="raise")

    away_df['Home-Away'] = 'Away'
    home_df['Home-Away'] = 'Home'
    
    headers = []
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')
    html = soup.find_all('div', class_ = 'box')
    
    for item in html:
        h2 =', '.join([x.get_text() for x in item.find_all('h2')])
        match =([x.get_text() for x in item.find_all('h1')])
        headers.append(h2)
    
    my_list = h2.split(',')
    my_list = [s for s in my_list if "Basic and Advanced Stats" in s]  

    my_list = [x.replace("Basic and Advanced Stats", '').replace("Basic and Advanced Stats", '') for x in my_list]
    away_team = my_list[0]
    home_team = my_list[1]
    away_df['Team'] = away_team
    home_df['Team'] = home_team
    frames = [away_df, home_df]
    df = pd.concat(frames)
    
    match = match[0]
    
    df['Match'] = match
    master_df = pd.concat([master_df, df], axis=0).reset_index(drop=True)
    master_df.to_excel('nba_dataset.xlsx', index=False)

