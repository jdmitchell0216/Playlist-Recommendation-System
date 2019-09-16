# Playlist-Recommendation-System
Playlist recommendation system with user to user implicit collaborative filtering.

This project retrieves user data from the Reddit and Spotify API's to suggest songs that would likely be good additions to existing playlists.

## Data Gathering
In order to obtain user playlists from the spotify API, spotify user IDs are required. To gather these IDs, I relied primarily on the subreddits r/Spotify and r/SpotifyPlaylists, where reddit users often post spotify playlists. PRAW, a python Reddit API wrapper, was used to search for posts that contained spotify media embeddings on these subreddits. Regex was then used to find the spotify user ID for the playlist. A diagram of this process can be seen below.

<p align="center">
  <img width="121" height="251" src="https://github.com/jdmitchell0216/Playlist-Recommendation-System/blob/master/images/playlist_rec_api_diagram.png">
</p>

The reddit API only allows searching a limited number of the most recent posts, but more user IDs can be found as more playlist posts are made.
