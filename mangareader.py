import cfscrape
import bs4 as bs
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pandas as pd

scraper = cfscrape.create_scraper() 

url_list = []
title_list = []
alternate_title = []
genres_list = []
writer_list = []
artist_list = []
summary_list = []
genres_list = []

url = 'https://www.mangareader.net/alphabetical'

try:
    content = str(scraper.get(url).content)
    soup = BeautifulSoup(content, "html.parser")
    for target in soup.find_all('li'):
        url_list.append(target)


    url_list2 = url_list[88:len(url_list)-11]

    start_title = '<li><a href="'
    end = '">'  

    i = 0
    for url in url_list2:
        url_list2[i] = 'https://www.mangareader.net'+(str(url).split(start_title))[1].split(end)[0]
        i += 1
except:
    pass

try:
    for url in url_list2: 
        print(url)
        sleep(2+randint(1,5))
        content = str(scraper.get(url).content)
        soup = BeautifulSoup(content, "html.parser")
        i = 0
        for target in soup.find_all('tr'):
            if i == 0:
                title_list.append(str(target.text.lower()).replace('\\n','').replace('name:','').strip())
            elif i == 1:
                alternate_title.append([str(target.text.lower()).replace('\\n','').replace('alternate name:','').replace(';',',')])
            elif i == 4:
                writer_list.append(str(target.text.lower()).replace('\\n','').replace('author:',''))
            elif i == 5:
                artist_list.append(str(target.text.lower()).replace('\\n','').replace('artist:',''))
            elif i == 7:
                genres_list.append(str(target.text.lower()).replace('\\n','').replace('genre:',''))
            elif i == 8:
                for target in soup.find_all('div', id='readmangasum'):
                    summary_list.append(str(target.text.lower()).replace('\\n','').replace('\\r\\',' '))
            i += 1  
except:
    pass

data = {
    'title' : title_list,
    'alternate_title' : genres_list,
    'genres' : genres_list,
    'writer' : writer_list,
    'artist':artist_list,
    'summary':summary_list
}

df = pd.DataFrame.from_dict(data)
df.to_csv('mangareader.csv')
print(df.head())
print(df.shape)               

