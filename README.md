# Spotify Music Suggestions

![SpotifyTaigaGIF.gif](Spotify%20Music%20Suggestions%204f33f06b37f240ada47329a6a621a240/SpotifyTaigaGIF.gif)

The rapid growth of online music streaming platforms has brought into the market a new range of global music suggestions, promoting cultural diversity and expanding people's music taste. Nowadays, music listeners are offered many choices, and sometimes, it can even be overwhelming to select and browse a long list of music suggestions.

Our project consists in creating a song recommender based on the audio features identified by Spotify. We aim to understand the patterns in music, and users listening habits, predicting the most relevant recommendations.

![meme-7-1.jpg](Spotify%20Music%20Suggestions%204f33f06b37f240ada47329a6a621a240/meme-7-1.jpg)

# **Challenge🔥**

Gnod is a website that provides recommendations for music, art, literature and digital products based on collaborative filtering algorithms. 
We were hired by Gnod to enhance their music recommendations for Gnoosic (Gnod’s flagship product for music recommendations).

Jane, Gnod’s CTO approached us to solve the following challenges:

- To enhance filtering algorithms
- To suggest songs from an acoustic point of view and popular songs around the world
- To suggest a song from the top 100 Billboard chart if the user is listening to a song present on that same chart.

![image (1).png](Spotify%20Music%20Suggestions%204f33f06b37f240ada47329a6a621a240/image_(1).png)

# **Data📄**

The data was gathered from 2 datasets, Kaggle web site and the Weekly Billboard Hot 100. 

In the notebook, our main goal was to build two song databases (one for Hot 100 songs from Billboard, the other one from Kaggle), get the features for each song, and create clusters to categorize and divide the songs.

We have used a dataset containing a sample of 20,000 songs, after the cleaning, we end up with a sample of 6,000 songs.

# **Sources🧭**

- https://www.billboard.com/charts/hot-100
- www.kaggle.com/datasets/sumitmohod22/songs-data-set

# **Music Features🎶**

The content filtering method is based on the analysis of song features. It determines which features are most important for suggesting the songs and in that way, the application adapts, learns the user-behavior and suggests the items based on that behavior.

Music Features:

- Danceability
- Energy
- Loudness
- Speeches
- Acoustics
- Instrumentals
- Liveness
- Valence
- Tempo

# **Cluster Analysis📦**

The best way of interpreting the clusters is to investigate the averages of features for every cluster.

In the table below you can see the averages of all input features.

| Clusters | Danceability | Energy | Acousticness | Instrumentalness | Valence |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.68 | 0.72 | 0.14 | 0.02 | 0.72 |
| 1 | 0.55 | 0.70 | 0.14 | 0.76 | 0.44 |
| 2 | 0.50 | 0.34 | 0.69 | 0.11 | 0.33 |
| 3 | 0.44 | 0.78 | 0.07 | 0.03 | 0.38 |

**In cluster 0 we can find songs like:**

| *Super Freaky Girl  | Nicki Minaj |*

| *As It Was | Harry Styles |*

| *About Damn Time | Lizzo |*

| *Break My Soul | Beyonce |*

This Cluster is mainly populated by an Energetic type of music.

It lacks on instrumental overall, but has a clear relation with danceability feature.

It will definitly make your body move! 

**In cluster 1 we can find songs like:**

*| Walking Through The Country | The Grass Roots |*

*| Tron | Foals |*

*| Tacobel Canon | Ratatat |*

*| Everywhere I Go | The Black Keys |*

This Cluster is populated by musics with a predominant Instrumental type.

It has the slowest music style among the other clusters with a little R&B and rock style.

**In cluster 2 we can find songs like:**

*| Running Up That Hill (A Deal With God) | Kate Bush |*

*| Alone | Rod Wave |*

*| Glimpse Of Us | Joji |*

*| Rock And A Hard Place | Bailey Zimmerman |*

In cluster 2 we can find more Acoustic musics.

The average values for acousticness are not very high, the overall dataset is mainly focused on dance/energetic music.

**In cluster 3 we can find songs like:**
*| The Kind Of Love We Make | Luke Combs |*

*| Titi Me Pregunto | Bad Bunny |*

*| Wasted On You | Morgan Wallen |*

*| Ghost | Justin Bieber |*

Cluster 3 presents us with a majority of Energetic type of songs.

Although it doesn’t has a great relation with danceability for sure you can expect an intense type of music.

### Conclusions

As this work is based on the music features, which are mostly technical indicators, provided by Spotify, the music genres output might not be according to your taste.

However the application has a very interesting behaviour and regardless the song suggestion it will always be a fun and unpredictable expirience, we recommend it😏

# **Built with 🖥️**

- Python
- Jupyter Notebook
- Pandas
- Scikit-Learn
- Matplotlib
- Dash
- Streamlite
- Spotipy

# ****Schema****

![Schema.jpg](https://github.com/JCabral88/Spotify_Music_Suggestions/blob/main/images/Schema.jpg?raw=true)
