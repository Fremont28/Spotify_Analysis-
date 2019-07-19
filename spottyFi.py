import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time 
import numpy as np 

#This script collects the style, tempo, and popularity (+more) of the artist using Spotify's Python API 

#client information 
client_id = 'xxxx
client_secret = 'xxxx'
client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#i. artist playlist -------
met1=sp.user_playlist('Spotify','37i9dQZF1DZ06evO3ALAcw')

#get names of playlist 
ids=[]
for i in met1['tracks']['items']:
    track=i['track']
    ids.append(track['id'])

#song features 
meta=sp.track(ids[0])
features=sp.audio_features(ids[0])

#key values 
for key in meta.keys():
    print(key)

name=meta['name']
album=meta['album']['name']
artist=meta['album']['artists'][0]['name']
rel_date=meta['album']['release_date']

avail_mrkts=meta['available_markets']

#ii. loop through playlist --------
def get_playlist(user,playlist_id):
    ids=[]
    playlist=sp.user_playlist(user,playlist_id)
    for item in playlist['tracks']['items']:
        track=item['track']
        ids.append(track['id'])
    return ids 

ids=get_playlist('this is parov stelar','37i9dQZF1DZ06evO3ALAcw')

#get song features 
def getTrackFeatures(id):
      meta = sp.track(id)
      features = sp.audio_features(id)

      # Meta
      name = meta['name']
      album = meta['album']['name']
      artist = meta['album']['artists'][0]['name']
      release_date = meta['album']['release_date']
      length = meta['duration_ms']
      popularity = meta['popularity']

      # Features
      acousticness = features[0]['acousticness']
      danceability = features[0]['danceability']
      energy = features[0]['energy']
      instrumentalness = features[0]['instrumentalness']
      liveness = features[0]['liveness']
      loudness = features[0]['loudness']
      speechiness = features[0]['speechiness']
      tempo = features[0]['tempo']
      time_signature = features[0]['time_signature']

      track = [name, album, artist, release_date, length, popularity, danceability, acousticness, danceability, energy, instrumentalness, liveness, loudness, speechiness, tempo, time_signature]
      return track

tracks = []
for i in range(0, 5):
    time.sleep(.5)
    track = getTrackFeatures(ids[i])
    tracks.append(track)

df = pd.DataFrame(tracks, columns = ['name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
    

#iii. artist comparisosn (i.e. similar artists, genres, popularity)-----------
birdy_uri = 'spotify:artist:5gCRApTajqwbnHHPbr2Fpi'
results=sp.artist_albums(birdy_uri,album_type='album')
albums=results['items']

while results['items']:
    results=sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])

related_artists=sp.artist_related_artists('5gCRApTajqwbnHHPbr2Fpi')
rX=related_artists 

#similar artistss 
names=[]
genres=[]
popularity=[] 
folls=[]

for i in range(0,20):
    name=rX['artists'][i]["name"]
    genre=rX['artists'][i]["genres"]
    pop=rX['artists'][i]['popularity']
    foll=rX['artists'][i]['followers']['total']
    names.append(name)
    genres.append(genre)
    popularity.append(pop)
    folls.append(foll)