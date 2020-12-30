# spotify-releases
A script to query new releases and popularity rankings from Spotify for a group of artists and store in a sqlite DB

<b>Methodology</b><br/>
The script loops through each artist within input .txt file and retrieves any <b>Albums</b>, <b>EPs</b>, <b>Singles</b>, or <b>Features</b> that each artist has released on Spotify within the specified time period<br/>
<br/>
Using SQL commands, an associated <i>'spotify.sqlite'</i> DB is created with individual tables for each category of release.<br/>
This sqlite Database contains 5 tables: 
- <i>Artist</i>
- <i>Albums</i>
- <i>EPs</i>
- <i>Singles</i>
- <i>Features</i>
<br/>
The tables are relationally linked by the 'id' Primary Key column in the <i>Artist</i> table, which corresponds to the column 'artist_id' in each other Table

### Using these tables, the following views can be created to categorize the newly released music
<b>New Album Releases</b><br/><br/>
![AlbumsView](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/albums_view.png)<br/><br/>
<b>New EP Releases</b><br/><br/>
![EPsView](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/eps_view.png)<br/><br/>
<b>New Single Releases</b><br/><br/>
![SinglesView](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/singles_view.png)<br/><br/>
<b>Newly Released Songs that the Artist is Featured on</b><br/><br/>
![FeaturesView](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/features_view.png)<br/><br/>

### The Artist Table can also be sorted by 'Popularity' to find the most popular artists in the population
![Popularity](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/artist_popularity.png)<br/><br/>

### Example imput of the .txt file
Artist URIs can be found on each artist's public Spotify profile<br/>
![artist_uris](https://github.com/Ben-Tiemeyer/spotify-releases/blob/main/images/artist_uris.png)<br/>
  
