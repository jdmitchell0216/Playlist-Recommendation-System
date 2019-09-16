# Playlist-Recommendation-System
Playlist recommendation system with user to user implicit collaborative filtering.

This project retrieves user data from the Reddit and Spotify API's to suggest songs that would likely be good additions to existing playlists.

## Data Gathering
In order to obtain user playlists from the spotify API, spotify user IDs are required. To gather these IDs, I relied primarily on the subreddits r/Spotify and r/SpotifyPlaylists, where reddit users often post spotify playlists. The python Reddit API wrapper PRAW was used to search for posts on these subreddits that contained spotify media embeddings. Regex was then used to find the spotify user ID for the playlist.

![data_gathering_flowchart](https://github.com/jdmitchell0216/Playlist-Recommendation-System/blob/master/images/playlist_rec_api_diagram.png)
