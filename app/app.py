import streamlit as st
import pandas as pd
import spotipy
import songrecommender
from spotipy.oauth2 import SpotifyClientCredentials
import plot
from PIL import Image
from config import *
import functions


#client_id = '76569ea3f0a14f3895d5fd418affe943'
#client_secret = 'cb44eb7389f84fba813f91433b4c425a'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id= client_id,
                                                           client_secret= client_secret))


st.title('IronZaaaam - Mood Enhancer :boom:')
st.markdown('#')
st.markdown("![Alt Text](https://media.giphy.com/media/3o6ZtjUZAD5Lf0QFLW/giphy.gif)")
st.markdown('#')




search_choices = ['Song', 'Artist']
search_selected = st.sidebar.selectbox('Do you want to search for a song or an artist? ', search_choices)

st.subheader('What song fits your current mood? :zany_face: :umbrella_with_rain_drops: :coffee:  :anger: :smiling_imp:')

search_keyword = st.text_input(search_selected)
button_clicked = st.button("Mood On  👈")
st.markdown('#')
st.subheader('Pick your song')


search_results = []
tracks = []
artists = []

if search_keyword is not None and len(str(search_keyword)) > 0:
    if search_selected == 'Song':
        tracks = sp.search(q='track:'+ search_keyword,type='track', limit=10)
        tracks_list = tracks['tracks']['items']
        
        if len(tracks_list) > 0:
            for track in tracks_list:
                str_local = track['name'] + " - BY - " + track['artists'][0]['name']
                search_results.append(str_local)
                #st.write(search_results)
        else:
            st.write('Are you sure this is a song?')

    elif search_selected == 'Artist':
        #st.write('Start artist search')
        artists = sp.search(q='artist:'+ search_keyword,type='artist', limit=10)
        artists_list = artists['artists']['items']
        if len(artists_list) > 0:
            for artist in artists_list:
                #st.write(artist['name'])
                search_results.append(artist['name'])


if search_selected == 'Song':
    selected_track = st.selectbox('Select your song: ', search_results)
    #st.write(selected_track)
    
if search_selected == 'Artist':
    selected_artist = st.selectbox('Select your artist: ', search_results)


if selected_track:
    tracks_list = tracks['tracks']['items']
    track_id = None
    if len(tracks_list) > 0:
        for track in tracks_list:
            str_temp = track['name'] + " - BY - " + track['artists'][0]['name']
            if str_temp == selected_track:
                track_id = track['id']
                track_album = track['album']['name']
                img_album = track['album']['images'][1]['url']
                songrecommender.save_album_image(img_album, track_id)
                #st.write(track_id)
                

    if track_id is not None:

        track_choices = ['My Mood in Features', 'Do Your Magic']
        
        selected_track_choice = st.sidebar.selectbox('Please select track choice: ', track_choices)

        track_features = sp.audio_features(track_id)
        df = pd.DataFrame(track_features, index= [0])
        df_features = df.loc[:, ['danceability', 'energy', 'acousticness', 'instrumentalness', 'valence']]

        
        if selected_track_choice == 'My Mood in Features':
            st.markdown('###')
            st.subheader('Your Song is featured in the Album: ')
            image = functions.get_album_image(track_id)
            st.image(image)
            st.markdown('#')
            st.subheader('Those are the Audio Features of your song: ')
            st.dataframe(df_features)
            functions.feature_plot(df_features)
            
        elif selected_track_choice == 'Do Your Magic':
            
            #st.subheader('Trust us with this one!!!!')
            
            similar_song_id = functions.app_check_song_on_df_and_make_suggestion(track_id, df_features)
            df, link = functions.get_spotify_link(similar_song_id)
            a_link = 'https://open.spotify.com/track/' + similar_song_id
            st.markdown('##')
            st.subheader(':hourglass: ..... analyzing your mood .... :hourglass:...mood recognized!')
            st.markdown('#')
            st.markdown('##')
            st.subheader('IronZaam.fit(:broken_heart: :broken_heart: :broken_heart:)')
            st.subheader('song_predict = IronZaaam.predict(mood)')
            st.subheader('print(song_predict)')
            
            st.write(df)
            st.markdown('##')
            
            
                       
            col1, col2, = st.columns(2)

            with col1:
                st.header("listen to the song on ")

                image = Image.open('img/spotify.png')
                st.image(image, caption='spotify')

            with col2:
                st.header("... SPOTIFY")
                st.write(a_link)
            st.markdown('#')
            image = Image.open('img/music.jpg')
            st.image(image, caption='music')
            
            st.markdown('##')
            st.subheader('THE BIG QUESTION is: .... Is this song Hot :hot_pepper: or Not :shit:???')
            st.markdown('##')
            st.subheader('1) import Hot_or_Not_Score()')
            st.subheader('2) score = IronZaaam.Hot_or_Not_Score(Mood, Song)')
            st.markdown('#')
            st.header('SCORE = :hot_pepper:')
            
           
else:
    st.write('Please select a song')






