from ytmusicapi import YTMusic

# Playlist ID of "All songs" playlist
all_songs_playlist_id = "PLz5HOyT_5fjLhK2N_oxbSPHqS_VSW2DBS"

# Create an authenticated YTMusic instance
yt = YTMusic("oauth.json")

# Get all playlist IDs (excluding the "All songs" playlist)
playlist_ids = [playlist.get("playlistId") for playlist in yt.get_library_playlists() if playlist.get("playlistId") != all_songs_playlist_id]

# Collect all songs from other playlists
all_other_songs = set()
for playlist_id in playlist_ids:
    songs = yt.get_playlist(playlistId=playlist_id).get("tracks", [])
    for song in songs:
        all_other_songs.add(song.get("videoId"))

# Get the songs currently in the "All songs" playlist
all_songs_playlist_songs = yt.get_playlist(playlistId=all_songs_playlist_id).get("tracks", [])
all_songs_playlist_ids = {song.get("videoId") for song in all_songs_playlist_songs}

# Find songs to add (in other playlists but not in the "All songs" playlist)
songs_to_add = all_other_songs - all_songs_playlist_ids

# Find songs to remove (in the "All songs" playlist but not in other playlists)
songs_to_remove = all_songs_playlist_ids - all_other_songs

# Add missing songs to the "All songs" playlist
if songs_to_add:
    yt.add_playlist_items(playlistId=all_songs_playlist_id, videoIds=list(songs_to_add))
    print(f"Added {len(songs_to_add)} songs to 'All songs' playlist.")

# Remove extra songs from the "All songs" playlist
if songs_to_remove:
    yt.remove_playlist_items(playlistId=all_songs_playlist_id, videoIds=list(songs_to_remove))
    print(f"Removed {len(songs_to_remove)} songs from 'All songs' playlist.")

print("Sync complete.")
