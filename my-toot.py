# Write some code to post a status on our timeline
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

#from datetime import datetime, date, time, timezone


load_dotenv()

mastodon = Mastodon(
        client_id=os.getenv("Client_key"),
        client_secret=os.getenv("Client_secret"),
        access_token=os.getenv("access_token"),
        api_base_url="https://mstdn.social"
)

# Set the variables here
xpl_date = 'April 21, 2025'
xpl_hashtag = 'AmusementPark'
xpl_toot_count = 19
xleaderboard = ['foo@example.com']
xhighscore = 6
xpl_id = 'PLZyP4b181sFas_yPu5LPS-rXKJjOeAdXr'


def my_toot(pl_date, pl_hashtag, pl_toot_count, leaderboard, highscore, pl_id):

    stp1 = 'Hi! Here is the KpopMonday compilation playlist for ' + pl_date
    stp2 = 'This week\'s theme is #' + pl_hashtag
    stp3 = 'Total number of toots for ' + pl_hashtag + ' is: ' + str(pl_toot_count)
    stp4 = 'Top contributor(s) this week with ' + str(highscore) + ' toots: ' + ', '.join(leaderboard)
    stp5 = 'https://youtube.com/playlist?list=' + pl_id
    stp6 = '#kpopmonday #kpop'

    # Leaving out leaderboard based on feedback
    status_text = '\n\n'.join((stp1, stp2, stp3, stp5, stp6))
    print(status_text)

    mastodon.status_post(status = status_text, visibility = "public")

my_toot(xpl_date, xpl_hashtag, xpl_toot_count, xleaderboard, xhighscore, xpl_id)