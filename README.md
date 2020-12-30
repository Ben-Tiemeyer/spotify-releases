# spotify-releases
A script to query new releases and popularity rankings from Spotify for a group of artists and store in a sqlite DB

<b>Methodology</b><br/>
The script loops through each artist within input .txt file and retrieves any Albums, EPs, Singles, or Features that each artist has released on Spotify within the specified time period<br/>
<br/>
An associated <i>'spotify.sqlite'</i> DB is created with individual tables for each category of release.<br/>
This sqlite DB contains 5 tables: <i>Artist</i>, <i>Albums</i>, <i>EPs</i>, <i>Singles</i>, <i>Features</i>
