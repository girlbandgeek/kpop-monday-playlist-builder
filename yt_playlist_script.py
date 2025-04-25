import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    # credentials = flow.run_local_server(port=35353)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    
    search_input = input("Please enter your search: "),

    # Search for 'Radiohead cover' videos
    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q = search_input,
        type="video"
    )
    response = request.execute()

    playlist_name = " ".join(search_input) + " Playlist"

    create_playlist_response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": "A playlist created with the YouTube API",
                "tags": ["sample playlist", "API call"],
                "defaultLanguage": "en"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    ).execute()

    # Specify your playlist ID here
    playlist_id = create_playlist_response["id"]

    # Add search results to the playlist
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        add_video_to_playlist(youtube, video_id, playlist_id)

def add_video_to_playlist(youtube, video_id, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    )
    response = request.execute()
    print(f"Added video {video_id} to playlist {playlist_id}")

if __name__ == "__main__":
    main()
