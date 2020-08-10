import cfscrape
import bs4 as bs
from bs4 import BeautifulSoup
from random import randint
from time import sleep
import pandas as pd


scraper = cfscrape.create_scraper() 
url_list = []
title_list = []
genres_list = []
publisher_list = []
writer_list = []
artist_list = []
summary_list = []
available_genres = []

start_title = 'https://readcomiconline.to/Comic/'
end = '</p>'

i = 0
while i <= 5:#406:#100 150 200 250 300 350 365:
    sleep(2+randint(1,2))
    url = 'https://readcomiconline.to/ComicList?page='+str(i)
    content = str(scraper.get(url).content)

    soup = BeautifulSoup(url, "html.parser")
    for url in soup.find_all('a', class_='bigChar'):
        url_list.append('https://readcomiconline.to'+str(url.get('href')))
    i += 1
url_list = list(set(url_list))
print(url_list)
title_list = []

start = '">'
end = '</a>'
start_summary = '<span class="info">Summary:</span>'
end_summary= '</p>'
start_link = '<a class="dotUnder" href="/'
end_link = '" title="'

i = 0
while i < len(url_list):
    print(i)
    genres = []
    publisher = []
    writer = []
    artist = []
    print(url_list[i])
    try:
        content = str(scraper.get(url_list[i]).content)
        soup = BeautifulSoup(content, "html.parser")
        summary = (str(soup).split(start_summary))[1].split(end_summary)[0]
        summary_value = str(BeautifulSoup(summary, "html.parser").text.replace("\\r\\n                            ", "").lower())
        summary_list.append(summary_value)
        title_list.append(str(url_list[i]).replace('https://readcomiconline.to/Comic/','').replace('-',' ').lower())
        for url in soup.find_all('a', class_='dotUnder'):
            clean = (str(url).split(start_link))[1].split(end_link)[0]
            if clean[0] == 'G':
                genres.append(clean.replace('Genre/','').lower())
            elif clean[0] == 'P':
                publisher.append(clean.replace('Publisher/','').lower())
            elif clean[0] == 'W':
                writer.append(clean.replace('Writer/','').lower())
            elif clean[0] == 'A':
                artist.append(clean.replace('Artist/','').lower())
        genres_list.append(genres)
        publisher_list.append(publisher)
        writer_list.append(writer)
        artist_list.append(artist)
        sleep(2+randint(1,3))
    except:
        pass

    i += 1

	
# Dictionary with list object in values
data = {
    'title' : title_list,
    'genres' : genres_list,
    'publisher' : publisher_list,
    'writer' : writer_list,
    'artist':artist_list,
    'summary':summary_list
}

df = pd.DataFrame.from_dict(data)
df.to_csv('readcomic5.csv')
print(df.head())
print(df.shape)
