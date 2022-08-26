import pandas as pd
import numpy as np
import time
from bs4 import BeautifulSoup
import requests
import yaml
from config import *
import pickle
import spotipy
import time
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret))


def scrap_hot100(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    if (response.status_code == 200):   
        title = []
        artists = []
        for i in soup.select("li.o-chart-results-list__item > h3"):
            title.append(i.get_text().strip())
        for i in soup.select("li.o-chart-results-list__item > span:nth-child(2)"):
            artists.append(i.get_text().strip())
        unwanted = {'NEW', 'RE-\nENTRY'}
        artists = [ele for ele in artists if ele not in unwanted]
        songs = {'title': title,
                'artist': artists}
        hot100 = pd.DataFrame(songs).reset_index(drop = True)
        
        hot100['artist'] = hot100['artist'].str.replace(' Featuring', ',')
        hot100['artist'] = hot100['artist'].str.replace(' &', ',')
        hot100['artist'] = hot100['artist'].str.replace(' With', ',') 
        
        hot100.to_csv(config['data']['hot_songs_file'], index=False)
    return hot100




def NotHotSongs():

    #read hot file
    hot = pd.read_csv(config['data']['hot_songs_file'])
    #Reading the Kaggle Dataset
    songs = pd.read_csv(config['data']['kaggle_file'])

    #Randomly select 20000 songs
    np.random.seed(config['random_choice']['seed'])
    row_index = np.random.choice(len(songs), config['random_choice']['selection'])
    nothot = songs.iloc[row_index]

    #drop uneccessary columns and duplicates
    nothot.drop(['user_id', 'song_id', 'listen_count', 'song'], axis = 1, inplace = True)
    nothot.drop_duplicates(inplace = True)

    #Cleaning the Strings
    nothot['title']= nothot['title'].str.replace('\\', '')
    nothot['title']= nothot['title'].str.replace('_', ',')
    nothot['title']= nothot['title'].str.replace("'", "")
    nothot['title'] = nothot['title'].str.replace(' /', ',')
    nothot['title'] = nothot['title'].str.replace('/', ',')

    nothot['artist'] = nothot['artist'].str.replace('\\', '')
    nothot['artist'] = nothot['artist'].str.replace('_', ',')
    nothot['artist'] = nothot['artist'].str.replace(' /', ',')
    nothot['artist'] = nothot['artist'].str.replace('/', ',')
    nothot['artist'] = nothot['artist'].str.replace(' Featuring', ',')
    nothot['artist'] = nothot['artist'].str.replace(' featuring', ',')
    nothot['artist'] = nothot['artist'].str.replace(' &', ',')
    nothot['artist'] = nothot['artist'].str.replace('.', '')
    nothot['artist'] = nothot['artist'].str.replace('$', 's')
    nothot['artist'] = nothot['artist'].str.replace('ft.', 'feat.')

    unwanted_words = ["Radio", "radio", "Album", "album", "version", 
                      "remix", "Version", "edit", "remix", "Remix", "acoustic", 
                      "Acoustic", "@", "Explicit", "Single", "Digital", "Remaster",
                      "Remastered", "Mix", "Edit"]
    mask = nothot.iloc[:, 0].str.contains(r'\b(?:{})\b'.format('|'.join(unwanted_words)))
    nothot = nothot[~mask]
    
    # checking whether the song is in both tables: 
    for index, row in hot.iterrows():
        df = nothot[(nothot['title'] != row['title']) & (nothot['artist'] != row['artist'])]

    df.to_csv(config['data']['not_hot_songs_file'])
        
    return df.reset_index(drop=True)




def split_dataframe_by_position(df, num_of_splits):
	"""
	Takes a dataframe and an integer of the number of splits to create.
	Returns a list of dataframes.
	"""
	chunks = []
	index_to_split = len(df) // num_of_splits
	start = 0
	end = index_to_split
	for split in range(num_of_splits):
	    temporary_df = df.iloc[start:end, :]
	    chunks.append(temporary_df)
	    start += index_to_split
	    end += index_to_split
	return chunks




def search_song(chunks):
    """
    Takes the split_dataframe_by_position() as input and searches for the song id in the spotify database. 
    The function returns a combined df with the songs, the id and the corresponding spotify link. 
    """    
    list_of_ids = []
    link = []
        
    # for each song-artist in each chunk,look for the id & link 
    # in the spotify database and append values to ID- and LINK- LIST
    for chunk in chunks:
        for index, row in chunk.iterrows():
            try:
                song = sp.search(q="track:"+row["title"]+" artist:"+row["artist"], market="ES", limit=1)
                list_of_ids.append(song['tracks']['items'][0]['id'])
                link.append(song['tracks']['items'][0]['artists'][0]['external_urls']['spotify'])
            except: 
                list_of_ids.append('404')
                link.append('404')  
                print('{}, Song {} from {} not found '.format(index, row['title'], row['artist']))
        time.sleep(31)
        
    #Combine the chunks back together:
    df = pd.DataFrame(chunks[0])
    for chunk in chunks[1:]:
        df = pd.concat([df, chunk], axis = 0)
    
    # Add the column 'ID'
    df['id'] = list_of_ids
    df['link'] = link
    
    # Filter the id column and select only the ones that have a valid ID
    df = df.loc[df['id'] != '404'].reset_index(drop=True)
        
    return df




def audio_features(chunks, label):
	"""
	Takes df and ids from search_song() as input and returns a combined dataframe with 
	selected audio features.
	"""    

	all_features = []

	# API request by chunk
	for chunk in chunks: 
	    for index, row in chunk.iterrows():
	        try:
	            features_dict = sp.audio_features(row['id'])[0]
	            all_features.append(features_dict)
	        except:
	             print('{}, features from song {} not found '.format(index, row['title']))
	        
	    time.sleep(30)     
	    
	#Combine the chunks back together:    
	df = pd.DataFrame(chunks[0])
	for chunk in chunks[1:]:
	    df = pd.concat([df, chunk], axis = 0)

	# Create features dictionary
	feature_df = pd.DataFrame()
	for dictionary in all_features:
	    dict_to_df = pd.DataFrame.from_dict(dictionary, orient='index').T
	    feature_df = pd.concat([feature_df, dict_to_df], axis = 0)
	        
	feature_df.drop(['time_signature', 'analysis_url', 'type'], axis = 1, inplace = True)

	df_clean = df.merge(feature_df, on = 'id')

	df_clean['label'] = label

	return df_clean




def check_song_on_df_and_make_suggestion(song_id):
	"""
    Checks whether the song chosen by the user is in our dataframe.
    If so, the function checks if the song belongs to the 100 Hot Songs
    Billboard or not, then suggests a song based on cluster. 

    If the song is not on our dataframe, suggests a song by cluster.
    """  
	df = pd.read_csv('songs_main_4.csv')

	if song_id in df['id'].values:
	    song_row = df.loc[df['id'] == song_id]

	    if song_row['label'].values == 'hot':
	        hot_songs = df.loc[(df['label'] == 'hot') & (df['id'] != song_id)]
	        cluster = hot_songs.loc[hot_songs['clusters'] == predicted_cluster]
	        song_recommended = cluster[['title','link']].sample()
	        return song_recommended.title.values[0], song_recommended.link.values[0]

	    else:
	        not_hot_songs = df.loc[(df['label'] == 'nothot') & (df['id'] != song_id)]
	        cluster = not_hot_songs.loc[not_hot_songs['clusters'] == predicted_cluster]
	        song_recommended = cluster[['title','link']].sample()
	        return song_recommended.title.values[0], song_recommended.link.values[0] 

	# If the song is not included in our df, recommend any song       
	else:
		hot_songs = df.loc[(df['label'] == 'hot')]
		cluster = hot_songs.loc[hot_songs['clusters'] == predicted_cluster]
		song_recommended = cluster[['title','link']].sample()
		return song_recommended.title.values[0], song_recommended.id.values[0]