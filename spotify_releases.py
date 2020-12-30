import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
import time
import datetime
import sqlite3
from json.decoder import JSONDecodeError


# Enter the 25-digit username for your Sptoify account (Can be found at 'Account Overview')
username = 'xxxxxxxxxxxxxxxxxxxxxxxx'

#Enter client id and client secret for your Spotify app once you have registered at developer.spotify.com
client_id = xxxxxxxx
client_secret = xxxxxxxx
try:
    token = util.prompt_for_user_token(username=username,client_id=client_id,client_secret=client_secret, redirect_uri='http://google.com/')
except:
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)

# Create our spotifyobject
spotifyObject = spotipy.Spotify(auth=token)

#print(json.dumps(VARIABLE, sort_keys=True, indent=4))

user = spotifyObject.current_user()

#Connect to or create a SQLite DB named 'spotiy.sqlite'
conn = sqlite3.connect('spotify.sqlite')
cur = conn.cursor()

#SQL statement to clear all previous results and tables, and create new blank tables for Artist, Albums, EPs, Singles, and Features
cur.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Albums;
DROP TABLE IF EXISTS EPs;
DROP TABLE IF EXISTS Singles;
DROP TABLE IF EXISTS Features;

CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE,
    popularity INTEGER,
    followers INTEGER,
    pic TEXT
);

CREATE TABLE Albums (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    album_name  TEXT,
    release_date   TEXT,
    tracks    INTEGER
);

CREATE TABLE EPs (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    ep_name  TEXT,
    release_date   TEXT,
    tracks    INTEGER
);

CREATE TABLE Singles (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    single_name  TEXT,
    release_date   TEXT
);

CREATE TABLE Features (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    other_name  TEXT,
    main_artist  TEXT,
    release_date   TEXT
);
''')

now = datetime.datetime.now()
year = str(now.year)
print(year)
month = str(now.month)
print(month)
day = str(now.day)
print(day)
nowdate = year+'-'+month+'-'+day
print('now',nowdate)

#Input which Year, Month, and Date you want to search back until to find all releases of specified artists
backyear = input('From which year? (xxxx) ')
backmonth = input('From which month? (xx) ')
backday = input('From which day? (xx) ')
backdate = backyear+'-'+backmonth+'-'+backday

#Connect to text file with artist URIs labeled 'artist_uris.txt'
fname = 'artist_uris.txt'
fhand = open(fname)
count = 0

#For each artist in text file, retrieve all releases in specified time window and store to sqlite DB
for artist_uri in fhand:
    print(count)
    count = count + 1
    artist_uri = str(artist_uri.rstrip())
    artist = spotifyObject.artist(artist_uri)
    artist_name = artist['name']
    print(artist_name)
    followers = artist['followers']['total']
    popularity = artist['popularity']
    try:
        pic = artist['images'][2]['url']
    except:
        pic = ''
    albums = spotifyObject.artist_albums(artist_uri)

    cur.execute('''INSERT OR IGNORE INTO Artist (name, popularity, followers, pic)
        VALUES ( ?, ?, ?, ?)''', ( artist_name, popularity, followers, pic) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist_name, ))
    artist_id = cur.fetchone()[0]

    conn.commit()

    for album in albums['items']:
        if album['release_date'] <= nowdate and album['release_date'] >= backdate:

            # album group
            if album['album_group'] == 'album':
                print('found an album')
                project_name = album['name']
                project_release = album['release_date']
                project_length = album['total_tracks']

                cur.execute('''INSERT INTO Albums (artist_id, album_name, release_date, tracks)
                VALUES ( ?, ?, ?, ? )''', (artist_id, project_name, project_release, project_length) )

                conn.commit()

            # EP group
            if album['album_group'] == 'single' and album['total_tracks'] >= 4:
                print('found an ep')
                ep_name = album['name']
                ep_release = album['release_date']
                ep_length = album['total_tracks']

                cur.execute('''INSERT INTO Eps (artist_id, ep_name, release_date, tracks)
                VALUES ( ?, ?, ?, ? )''', (artist_id, ep_name, ep_release, ep_length) )

                conn.commit()

            # single group
            if album['album_group'] == 'single' and album['total_tracks'] <= 3:
                print('found a single')
                single_name = album['name']
                single_release = album['release_date']

                cur.execute('''INSERT INTO Singles (artist_id, single_name, release_date)
                VALUES ( ?, ?, ? )''', (artist_id, single_name, single_release) )

                conn.commit()

            # appears on group
            if album['album_group'] == 'appears_on':
                other_name = album['name']
                other_release = album['release_date']
                collab = album['artists'][0]['name']


                cur.execute('''INSERT INTO Features (artist_id, other_name, main_artist, release_date)
                VALUES ( ?, ?, ?, ? )''', (artist_id, other_name, collab, other_release) )

                conn.commit()

print('Retrieved',count,'Artists')

#Code to create views to combine artist tables with album/ep/singles tables

#SELECT Artist.popularity, Artist.name, Singles.single_name, Singles.release_date
#FROM Artist JOIN Singles
#ON Singles.artist_id = Artist.id
#ORDER BY Artist.popularity DESC, Artist.name, Singles.single_name, Singles.release_date

#SELECT Artist.popularity, Artist.name, Albums.album_name, Albums.tracks, Albums.release_date
#FROM Artist JOIN Albums
#ON Albums.artist_id = Artist.id
#ORDER BY Artist.popularity DESC, Artist.name, Albums.album_name, Albums.tracks, Albums.release_date

#SELECT Artist.popularity, Artist.name, Eps.ep_name, Eps.tracks, Eps.release_date
#FROM Artist JOIN EPs
#ON Eps.artist_id = Artist.id
#ORDER BY Artist.popularity DESC, Artist.name, Eps.ep_name, Eps.tracks, Eps.release_date

#SELECT Artist.popularity, Artist.name, Features.other_name, Features.main_artist
#FROM Artist JOIN Features
#ON Features.artist_id = Artist.id
#ORDER BY Artist.popularity DESC, Artist.name, Features.other_name, Features.main_artist
