import os
import spotipy
import spotipy.util as util
import requests
import numpy as np

os.environ["SPOTIPY_CLIENT_ID"] = "CILENT-ID-HERE"
os.environ["SPOTIPY_CLIENT_SECRET"] = "CLIENT-SECRET-HERE"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8080"

scope = "user-library-read playlist-modify-public playlist-modify-private playlist-read-private user-top-read"
uri = "http://localhost:8080"
username = "USERNAME-HERE"
token = util.prompt_for_user_token(username, scope, os.environ["SPOTIPY_CLIENT_ID"], os.environ["SPOTIPY_CLIENT_SECRET"], uri)
sp = spotipy.Spotify(auth=token)

playlist_name = "PLAYLIST-NAME-HERE"

try:
    top = sp.current_user_top_tracks(limit=20, time_range="long_term")

    nTrackName = []
    nTrackArtists = []
    nTrackID = []

    i = 0
    while i < 20:
        nTrackName.append(top["items"][i]["name"])
        nTrackArtists.append(top["items"][i]["artists"][0]["name"])
        nTrackID.append(top["items"][i]["id"])
        print(nTrackName[i] + " by " + nTrackArtists[i].upper())
        # print(top["items"][i]["external_urls"]["spotify"])
        i = i + 1

    x = False
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:  # filter for newly created playlist
            playlist_id = playlist['id']
            #print("here: ", playlist_id)   # if exists, print current playlist ID
            x = True
            delete = sp.user_playlist_replace_tracks(username, playlist_id, tracks=[])
            add = sp.user_playlist_add_tracks(username, playlist_id, tracks=nTrackID)
            print("ALL TRACKS UPDATED!")


    if x == False:
        create = sp.user_playlist_create(username, playlist_name, public=True, collaborative=False,
                                         description="DESCRIPTION-HERE")
        playlist_id = ''
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:  # filter for newly created playlist
                playlist_id = playlist['id']
                #print("new: ", playlist_id)    # if doesn't exist, print new playlist ID created
                add = sp.user_playlist_add_tracks(username, playlist_id, tracks=nTrackID)
                print("ALL TRACKS ADDED!")

except:
    print("fail")
