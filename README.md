# spotify-releases
A script to query new releases and popularity rankings from Spotify for a group of artists and store in a sqlite DB

<b>Methodology</b><br/>
The script loops through each artist within input .txt file and retrieves any Albums, EPs, Singles, or Features that each artist has released on Spotify within the specified time period<br/>
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
<b>New Album Releases</b><br/>
<b>New EP Releases</b><br/>
<b>New Single Releases</b><br/>
<b>Newly Released Songs that the Artist is Featured on</b><br/>

### The Artist Table can also be sorted by 'Popularity' to find the most popular artists

  
