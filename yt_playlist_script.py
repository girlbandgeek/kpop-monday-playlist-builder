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
    
    '''
    search_input = input("Please enter your search: "),

    # Search for 'Radiohead cover' videos
    request = youtube.search().list(
        part="snippet",
        maxResults=10,
        q = search_input,
        type="video"
    )
    response = request.execute()
    
    print("Search request output:")
    print(response)
    '''
    
    # playlist_name = " ".join(search_input) + " Playlist"
    playlist_name = "KpopMonday Playlist for 2025-03-24: wantuback"

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
                "privacyStatus": "public"
            }
        }
    ).execute()
    
    print("Playlist response output:")
    print(create_playlist_response)

    # Specify your playlist ID here
    playlist_id = create_playlist_response["id"]

    '''
    # Add search results to the playlist
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        add_video_to_playlist(youtube, video_id, playlist_id)
    '''
    
    # Add videos to playlist_id
    video_list = ['FxXCVxFZf2Q', 'wxs_Q2LFWNs', '-OBNH4V1Gv4', 'Uh_6PY9am_0', 'hF6Wds75rjg', 'y3KSD5sI0OM', 'Y9XXGztRM4Y', 'f5C-nNXUj_I', 'J6LAzgZi8N8', 'CeT--DbjtQI', '1mg1MRiky3o', 'Sa7QfiKGvfk', 'EiVmQZwJhsA', 'akPDKYwIoVk', 'fQj3jh90Q5s', 'URPYRLiGAnY', 'QDcfQQEhlJw', 'TnJqGMW4yts', '5LCGn9UFNAY', '28naAblMZmA', 'WM9DCnxXstI', 'IIj7j7mtNS4', 'sno_genwMz8', 'oL2AlXWVbKU', '6tK0XUQQ3wA', 'napCk8ZVlpw', 'Y_6VfzBl7yk', 'NpTpEsE9G8c', 'P5uE7KDkDFE', 'PvpRcDgd5jo', '9d9q-uTNKa4', 'J41qe-TM1DY', 'xnku4o3tRB4', 'vVBF6ZjS_Y8', '0lSSIQ4lE78']
    for video_id in video_list:
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
