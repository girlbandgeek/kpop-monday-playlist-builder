# Pull selected statuses with Mastodon API and process them
from mastodon import Mastodon
import datetime
from datetime import date
from datetime import timedelta
from datetime import time
from dateutil import parser
from dotenv import load_dotenv
import os
import sys
import re
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# Define some variables
start_buffer = timedelta(hours=2)  # Bonus time *before* 00:00
# tz_adjust = timedelta(hours=-7)  # Set to -7 for computer in Pacific time
tz_adjust = timedelta(hours=0)  # Set to -7 for computer in Pacific time
# day_len = timedelta(days=1, hours=12)  # Total length of kpopmonday, e.g. 36 hrs
day_len = timedelta(days=2, hours=4)  # Total length of kpopmonday, e.g. 36 hrs; bumping up for late folks
# List of accounts not to include, e.g. not our own user and possibly others to block ;)
excluded_users=['kpopmondayplaylistbot@mstdn.social']
# Google API related:
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]


load_dotenv()

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

# Function to retrieve statuses from Mastodon
def retrieve_statuses(hhtag, mmy_min, mmy_max, since_stat, max_key):
    print("hhtag", "mmy_min", "mmy_max", "since_stat", "max_key")
    print(hhtag, mmy_min, mmy_max, since_stat, max_key)
    hashtag_posts={}
    # There will be 2 different "mastodon.timeline_hashtag" calls, depending on whether since_id has been set...
    # This is part of recursive logic, to handle API limit of ~20 statuses retrieved per call
    if since_stat == "":
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = mmy_min, max_id = mmy_max)
    else:
        hashtag_posts=mastodon.timeline_hashtag(hashtag = hhtag, min_id = since_stat, max_id = mmy_max)

    # convert list to dict
    hashtag_dict = [(index, item) for index, item in enumerate(hashtag_posts)]
    hashtag_dict = dict(hashtag_dict)

    # define a dict to contain the output
    results_dict={}
    
    for key, value in hashtag_dict.items():
        rlist=[]

        print(f"record number: ", key)
        print(f"status id: ", hashtag_dict[key]["id"])
        print(f"created_at: ", hashtag_dict[key]["created_at"])
        print(f"account id: ", hashtag_dict[key]["account"]["id"])
        print(f"account name: ", hashtag_dict[key]["account"]["acct"])
        
        # rlist.append(hashtag_dict[key]["id"])
        rlist.append(hashtag_dict[key]["created_at"])
        rlist.append(hashtag_dict[key]["account"]["id"])
        rlist.append(hashtag_dict[key]["account"]["acct"])

        ccontent = hashtag_dict[key]["content"]

        match = re.findall(r'(www\.youtube\.com/watch\?v=|youtu\.be/)([\w-]+)', ccontent)
        if len(match) > 0: 
            print(f"videos: ", match)
            vid_list=[]
            for iitem in match:
                vid_list.append(iitem[1])
            # remove duplicate videos
            new_vid_list = list(set(vid_list))
            print("video ID's: ", new_vid_list)
            rlist.append(new_vid_list)
        else:
            print(f"videos: NOT MATCHED!!!")
            rlist.append([])

        # Generate a list of tags      
        tag_dict = hashtag_dict[key]["tags"]
        tag_list=[]
        for x in tag_dict:
            tag_list.append(x["name"])
            # print(f"name of the tag: ", x["name"])
        print(f"tag_list: ", tag_list)
        
        # we will use the status id as the dict key
        # Make sure we are getting only #kpopmonday statuses and also,
        # Exclude statuses from list of excluded users
        if "kpopmonday" in tag_list and hashtag_dict[key]["account"]["acct"].lower() not in excluded_users:
            kd_key = hashtag_dict[key]["id"]
            results_dict[kd_key] = rlist
        else:
            continue    # skip if desired conditions not met         
        
    # Remove potential duplicate record 
    if max_key in results_dict.keys():
        del results_dict[max_key]

    return results_dict

# Function to create to playlist on YouTube
def playlist_create(pl_videos, pl_datestring, pl_hashtag):
    # Disable OAuthlib's HTTPS verification when running locally.
    # DO NOT leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"

    # Get credentials and create an API client
    # This is original way, requiring local browser:
    '''
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    # credentials = flow.run_local_server(port=35353)

    '''
    
    # This is new way, which uses browser on different machine from
    # where the script is running
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes, redirect_uri='urn:ietf:wg:oauth:2.0:oob')

    # Tell the user to go to the authorization URL:
    auth_url, _ = flow.authorization_url(prompt='consent')
    print('Please go this URL: {}'.format(auth_url))

    # The user will get an authorization code. This code is used to get the
    # access token.
    code = input('Enter the authorization code: ')
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Credentials acquired, create the client connection
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

# Function to post the final status
def my_toot(pl_date, pl_hashtag, pl_toot_count, leaderboard, highscore, pl_id):

    stp1 = 'Hi! Here is the KpopMonday compilation playlist for ' + pl_date
    stp2 = 'This week\'s theme is #' + pl_hashtag
    stp3 = 'Total number of toots for ' + pl_hashtag + ' is: ' + str(pl_toot_count)
    stp4 = 'Top contributor(s) this week with ' + str(highscore) + ' toots: ' + leaderboard
    stp5 = 'https://youtube.com/playlist?list=' + pl_id
    stp6 = '#kpopmonday #kpop'

    # Leaving out leaderboard based on feedback
    status_text = '\n\n'.join((stp1, stp2, stp3, stp5, stp6))
    print(status_text)

    mastodon.status_post(status = status_text, visibility = "public")

###  MAIN SCRIPT EXECUTION  ###
htag = sys.argv[1]
start_date = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
start_date_str=start_date.strftime("%B %d, %Y")    # Generate a string for later
t_time = time(0, 0)  # minutes, seconds
start_date = datetime.datetime.combine(start_date, t_time)
# Implement date, time adustments
my_min = start_date - start_buffer + tz_adjust
my_max = my_min + day_len
# For first go, set since_status to null:
since_status=""
output_dict={}
max_key='0'

while(True):
    records_to_add=retrieve_statuses(htag, my_min, my_max, since_status, max_key)

    if len(records_to_add) == 0:
        print("Records to add = 0")
        break

    # find latest record
    max_key = max(records_to_add, key=records_to_add.get)
    #since_status=parser.parse(records_to_add[max_key][0])
    since_status=(records_to_add[max_key][0])
    print(f"max_key: ", max_key, "since_status: ", since_status, "max_key: ", max_key)
    output_dict.update(records_to_add)

# if needed for trouble shooting:
# print("output_dict:")
# print(output_dict)

# Let's explore the relations betweeen the statuses and the timestamps
ccount=0
for key in sorted(output_dict.keys()):
    ccount=ccount+1
    print("RECORD: ",ccount, key, output_dict[key][0], output_dict[key][1], output_dict[key][2])

# Build the list of playlist videos, and Generate some 
# stats for this collection of statuses
playlist_vids = []
stats_dict = {}
der_count=0
for key in sorted(output_dict.keys()):
    if output_dict[key][3] != []:
        for i_item in output_dict[key][3]:
            if i_item not in playlist_vids:    # check for duplicates
                playlist_vids.append(i_item)
            else:
                continue
    # playlist_vids.append(output_dict[key][3])
    if output_dict[key][2] in stats_dict.keys():
        stats_dict[output_dict[key][2]] = stats_dict[output_dict[key][2]] + 1
    else:
        stats_dict[output_dict[key][2]] = 1
        
leader_count = max(stats_dict.values())
leader_board = ""
for key, value in stats_dict.items():
    if value == leader_count:
        if leader_board == "":
            leader_board = key
        else:
            leader_board = leader_board + ', ' + key
    else:
        continue


print(f"Total number of posts for ", htag, "is: ", ccount)
print(f"Top contributor(s) this week with", leader_count, "posts are: ", leader_board)
print(f"Playlist videos :", playlist_vids)

print(f"Generate playlist for ", htag)
video_identifier=playlist_create(playlist_vids, start_date_str, htag)

# Make the toot to our bot account
# my_toot(start_date_str, htag, ccount, leader_board, leader_count, video_identifier)

