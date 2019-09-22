# Playlist-Recommendation-System
Playlist recommendation system with user to user implicit collaborative filtering.

This project retrieves user data from the Reddit and Spotify API's to suggest songs that would likely be good additions to existing playlists.

## Data Gathering
In order to obtain user playlists from the spotify API, spotify user IDs are required. To gather these IDs, I relied primarily on the subreddits r/Spotify and r/SpotifyPlaylists, where reddit users often post spotify playlists. PRAW, a python Reddit API wrapper, was used to search for posts that contained spotify media embeddings on these subreddits. Regex was then used to find the spotify user ID for the playlist. A diagram of this process can be seen below.

<p align="center">
  <img width="121" height="251" src="https://github.com/jdmitchell0216/Playlist-Recommendation-System/blob/master/images/playlist_rec_api_diagram.png">
</p>

The reddit API only allows searching a limited number of the most recent posts, but more user IDs can be found as more playlist posts are made. A summary of the current database can be seen in the table below.

<p align="center">
  <img width="275" height="127" src="https://github.com/jdmitchell0216/Playlist-Recommendation-System/blob/master/images/data_summary_9_15_19.png">
</p>


## Recommendations
The recommendation system works by first having the user create a playlist of one or more songs. This playlist is then added to the database of playlists and a sparse matrix containing playlists and songs is created. The playlists' similarities are then found using sklearn's cosine similarity. The cosine similarity of each playlist to the input playlist is appended to the data for every song in the database. These scores are then aggregated and the tracks with the highest cumulative similarities are then returned to the user as recommendations. Currently, there are two versions for calculating similarities based on the method of aggregation. The first uses the sum of the similarities and the second uses the mean. The sum version will favor songs that occur more frequently in the database, while the mean will account for song frequency. The sum version should be used if you want song popularity to influence your recommendations, while the mean version should be used if you want songs to be recommended regardless of popularity.
