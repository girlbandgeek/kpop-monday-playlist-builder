# kpop-monday-playlist-builder
Create a YouTube playlist from videos submitted to a hashtag on Mastodon.

## Summary
This is a little script I hacked together for fun as a result of my participation in the KpopMonday hashtag on Mastodon. Each week on Monday a theme is posted, and participants post YouTube videos of K-pop songs that match the theme. I thought it would be fun to create a playlist for each week and post it at a dedicated bot account. This script is the result of that effort.

## General Requirements
- Recent python3 (I am running this with python 3.12.3 on MacOS 11.7.10)
- modules: Mastodon.py, dotenv
- google specific modules: google-auth, google-auth-oauthlib, google-api-python-client
 
## Mastodon Requirements
- Account on a Mastodon server
- In the Mastodon account, add an application with read/write privilege and generate the API keys
- Add the Client_key, Client_secret, and access_token in the .env file as shown in env.EXAMPLE
- Keep these secrets safe, and do not post in code repository or other insecure location

## Google Requirements
- Install the google specific modules noted above
- You need to have a google account. Log in and access the cloud console:
- https://console.cloud.google.com/auth/clients
- In the cloud console, you will need to create a client of type Desktop
- Download the Client secret json file, and save it as "client_secrets.json" in the root of the kpop-monday-playlist-builder folder
- As with the Mastodon secrets, the google client secrets should be secured to prevent unauthorized access to your account
- Because I am only going to use this to create playlists in my own account, I set the status to "Testing" and added my google account to the list of test users. This gets around further validation steps that are beyond the scope of my effort. Otherwise an Oauth error is generated and inserting the playlist in YouTube fails.

## Other Caveats
- Initially I conceived of this as a fully automated process that could run in a cron job without human intervention.
- The current implementation requires human interaction to kick off the script, and complete the YouTube authorization.
- Google API quota limits your account to 200 "insertions" per day; each playlist created and each video added is one insertion. It follows that if you have a big playlist, or test a lot in one day you can exceed your quota for that day.
- There is some hardcoded stuff for the timedate parameters used when making Mastodon API calls based on my particular use case; KpopMonday starts an hour or two before 00:00 GMT, and I check for 36 hours after that to catch all relevant toots. The timezone setting of the computer where the script runs needs to be accounted for as well.
- If you're running this on a Mac, avoid using the system Python. I had good luck using pyenv. This is a good pyenv resource: https://realpython.com/intro-to-pyenv/

## Installation

## Running the Script

## Acknowledgments
- This video got me started with the Mastodon api: https://www.youtube.com/watch?v=W3kb6aImHf8
- Then I found the Mastodon.py module, which is fully featured and has documentation here: https://mastodonpy.readthedocs.io/en/stable/index.html
- The YouTube playlist generation is largely lifted from https://github.com/umutulay/youtube-playlist-automation
- Thanks to the Mastodon K-pop fandom and @Erzbet@apobangpo.space who decides the weekly theme - you bring joy to my life!
