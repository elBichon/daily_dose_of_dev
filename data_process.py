import pandas as pd
df = pd.read_csv('readcomic1.csv')

i = 0
id_list = []
while i < len(df.title.values.tolist()):
	id_list.append(i)
	i += 1 

i = 0
summary_list = []
summary = df.summary.values.tolist()
while i < len(df.summary.values.tolist()):
	summary[i] = summary[i].replace(',','').replace("\'","").replace('’','').replace('n/a','')
	summary_list.append(summary[i])
	i += 1 

i = 0
title_list = []
title = df.title.values.tolist()
while i < len(df.title.values.tolist()):
	title[i] = title[i].replace(',','')
	title_list.append(title[i])
	i += 1 

data = {'id':id_list,'title':title_list,'summary':summary_list}
df = pd.DataFrame.from_dict(data)
df.to_csv('comic.csv')

df = pd.read_csv('readcomic1.csv')
artist = df.artist.values.tolist()
artist_list = []
id_list = []
i = 0
while i < len(artist):
	j = 0
	current_artist = artist[i].split(',')
	while j < len(current_artist):
		artist_list.append("'"+current_artist[j]+"'")
		id_list.append(i)
		j += 1
	i += 1
data = {'id_comic':id_list,'artist':artist_list}
df = pd.DataFrame.from_dict(data)
df.to_csv('artist.csv')

df = pd.read_csv('readcomic1.csv')
genres = df.genres.values.tolist()
genres_list = []
id_list = []
i = 0
while i < len(genres):
	j = 0
	current_genres = genres[i].split(',')
	while j < len(current_genres):
		genres_list.append(current_genres[j])
		id_list.append(i)
		j += 1
	i += 1
data = {'id_comic':id_list,'genres':genres_list}
df = pd.DataFrame.from_dict(data)
df.to_csv('genres.csv')

df = pd.read_csv('readcomic1.csv')
publisher = df.publisher.values.tolist()
publisher_list = []
id_list = []
i = 0
while i < len(publisher):
	j = 0
	current_publisher = publisher[i].split(',')
	while j < len(current_publisher):
		publisher_list.append(current_publisher[j])
		id_list.append(i)
		j += 1
	i += 1
data = {'id_comic':id_list,'publisher':publisher_list}
df = pd.DataFrame.from_dict(data)
df.to_csv('publisher.csv')

df = pd.read_csv('readcomic1.csv')
writer = df.writer.values.tolist()
writer_list = []
id_list = []
i = 0
while i < len(writer):
	j = 0
	current_writer = writer[i].split(',')
	while j < len(current_writer):
		writer_list.append("'"+current_writer[j]+"'")
		id_list.append(i)
		j += 1
	i += 1
data = {'id_comic':id_list,'writer':writer_list}
df = pd.DataFrame.from_dict(data)
df.to_csv('writer.csv')

