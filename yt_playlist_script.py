import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def playlist_create(pl_videos, pl_datestring, pl_hashtag):
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
    
    # playlist_name = " ".join(search_input) + " Playlist"
    playlist_name = "KpopMonday Playlist for " + pl_datestring + ":" + pl_hashtag

    create_playlist_response = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": playlist_name,
                "description": "A playlist created with the YouTube API for KpopMonday",
                "tags": ["kpop", "kpopmonday"],
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

    # Add videos to playlist_id
    for video_id in pl_videos:
	    add_video_to_playlist(youtube, video_id, playlist_id)
	    
    return playlist_id
    
def add_video_to_playlist(youtube, video_id, playlist_id):
    try:
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
    except:
        print(f"Unable to add video with id: ", video_id)    
    '''
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
    '''

video_list = ['74RzHIpZuDY', 'fCrCUv6rQ7I', 'Yb7tgdg4Wr4', 'R9VDPMk5ls0', 'W761DtH1oRg', 'nlnMDttgTbk', 'GEo5bmUKFvI', '-dxXa3rr11w', 'evBAiaYal1o', 'RyJlZy3SU6k', 'dp0F18FFCTE', 'q-67jToInT0', 'jTw-dBGb-9g', 'JYDL9elacQ8', 'gdZLi9oWNZg', '4bnIb1JJHdA', 'ON9_T5DnMr8', 'MmNDtLJGum8', '43r6lXilbcQ', 'wSDvWny60IU', 'CdfGsNgb0oI', '_O00298opt0', '8nJp1ETfkGw', 'zDhU4rhLEDY', 'Se6lN0a4-28', 'BCCR2LzlX90', 'uuLC6wfVA8Q', '1yvic9sAg64', 'RRf4DIvUIt0', 'GHPlerzZQKU', 'u4iDL3c0T1c', 'btDd9rOlc2k', 'KSH-FVVtTf0', 'bTTczRe-Pj0', 'SGfW8sophcQ', 'oSC47Yp-Hpg', '7wcM9Eq3UbI', 'B2kgWO6GgJM', 'MSrYGQUXrJ8', 'b-7NpUxW9bs', 'Dy8UXAi8BUc', 'FJ8kJdTYj1o', 'aqwJNSi0E84', 'MhySKtz2PT0', 'xD6VjvfcBIs', 'mJcjXjYWI6E', '71c1dJBL-DU', 'brCsmmAlsck', 'PQjovLrnvVo', 'meQvDHBSxbQ', 'GywDFkY3z-c', '0heWyFJ6bsA', 'DtkCP45ChvA', '0bIRwBpBcZQ', 'uho3n38lq7o', 'FrCz6qvPJXE', 'AFJ8Qg9HqR4', 'o3TDVRuMrR4', '13DSV6syufo', 'tct-9S4A56E', 'QQL8_OqewsY', 'X-iJZ0gfKPo', 'ArSW24-98Ts', 'r--HBv-SVls', 'T1tlmh0Nm5Q', 'b-9GNw-_1LA', 'OJCh090JnRg', 'KNWLQI5_JLc', 'bNKXxwOQYB8', 'PfOtieDrDkA', '00tUzCOPI6g', 'UNFk6_to5_0', 'jwVaKaa99L4', '373bbkRwIYk', 'Jm6MffkX36k', 'TP56DuUpKBE', 'jG5IyiVgaxA', 'sGRv8ZBLuW0', 'yJDc5vYw_UE', 'uR8Mrt1IpXg', 'r_II-nzTASw', 'FKlGHHhTOsQ', 'ThI0pBAbFnk', 'Jm6MffkX36k', 'uLjUBC4HpVQ', 'NB5jyYD2WEw', '1QD0FeZyDtQ', 'KA6GyYVOELA', 'gH14nS5NC0g', 'Q_TzqcWKz00', 'eKp5CAsKzmg', 'tZYsvAoSNxQ', 'v202rmUuBis', 'ANLjX94ICa0', 'eD8NC174Jik', 'RPhuQj8VRPE', 'Hs8QGv2VqJA', 'sno_genwMz8', 'lFiH2yUpWTk', '9RUeTYiJCyA', 'aScoiOoFces', 'PEKkdIT8JPM', 'cHwoSiXO-MI', 'RNj-GhxPM0g', 'keUi4wTX5MI', 'n8I8QGFA1oM', 'LYUKv2LOgzU', 'nRXqf7mBJtY', 'Ewp7t_llpSQ', 'sE5YAXaIypo', 'ZAEqQPAEkug', '0o45hUReYpA', 'Ulemhb5TyNk', 'G1ojcRTiu5g', 'nKU4OVH18mE', '-NGoD8l-fp4', '4Njp-J2s5uw', '15-Us6br1JY', 'PYEOubLoXDo', 'pfMiX36Xv68', 'Bk1EkF927hE', 'VDveYoETsKM', 'XqpzPhUWmh8', '_fex-Fz3t2g', 'itumySYySCo', 'ZncbtRo7RXs', 'D8VEhcPeSlc', 'b4HIIbKZZm8', 'skZxb5sBoiU', 'MwlKalNwGdk', '1nCLBTmjJBY', 'n6B5gQXlB-0', 'i0RCcSBPjuU', '1IVF2rqZKkk', '1pBgMBBsv4k', 'BVVfMFS3mgc', '17cLtAbB6ow', 'LYS-GygGAe4', 'p1sUg87QjV8', '30VMl9ZkmgE', 'Zbm5USVQQdk', '8BBF3vRY85M', 'nlnMDttgTbk', 'DiHUEWBRQEI']
date_start = "2024-12-02"
htag = "TwoSongsOneTitle"

playlist_id=playlist_create(video_list, date_start, htag)
print(f"Playlist id: ", playlist_id)
