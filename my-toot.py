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


xpl_date = 'April 21, 2025'
xpl_hashtag = 'AmusementPark'
xpl_toot_count = 19
xleaderboard = ['pixelcats@apobangpo.space']
xhighscore = 6
xpl_id = 'PLZyP4b181sFas_yPu5LPS-rXKJjOeAdXr'

'''
xpl_date = 'April 14, 2025'
xpl_hashtag = 'WaterFight'
xpl_toot_count = 24
xleaderboard = ['Erzbet@apobangpo.space', 'JillsJoy@nerdjoy.social']
xhighscore = 5
xpl_id = 'PLZyP4b181sFakZuWBPxY2WG5-py7Rq8YH'

xpl_date = 'April 07, 2025'
xpl_hashtag = 'WonAndOnly'
xpl_toot_count = 26
xleaderboard = ['Erzbet@apobangpo.space', 'abuelaskpop@kpop.social']
xhighscore = 4
xpl_id = 'PLZyP4b181sFZsi6k8_wi7meZ_zzuZ2djD'

xpl_date = 'March 31, 2025'
xpl_hashtag = 'StormSongs'
xpl_toot_count = 9
xleaderboard = ['Erzbet@apobangpo.space', 'nikunashi@ieji.de']
xhighscore = 2
xpl_id = 'PLZyP4b181sFa-9yrPSWB_YQwPntmEJXyI'

xpl_date = 'March 24, 2025'
xpl_hashtag = 'WantUBack'
xpl_toot_count = 30
xleaderboard = ['abuelaskpop@kpop.social']
xhighscore = 10
xpl_id = 'PLZyP4b181sFaE23njQeWlP68ixdMr2PKw'

xpl_date = 'March 17, 2025'
xpl_hashtag = 'VideoGame'
xpl_toot_count = 29
xleaderboard = ['Erzbet@apobangpo.space']
xhighscore = 6
xpl_id = 'PLZyP4b181sFbb8JZInop6d7dYXhiXfCbq'

xpl_date = 'March 10, 2025'
xpl_hashtag = 'SoloLadiesOfKpop'
xpl_toot_count = 42
xleaderboard = ['Erzbet@apobangpo.space', 'pixelcats@apobangpo.space']
xhighscore = 8
xpl_id = 'PLZyP4b181sFaMKPEDjIE9glk62s_LnOcV'

xpl_date = 'March 03, 2025'
xpl_hashtag = 'CatAndDog'
xpl_toot_count = 35
xleaderboard = ['abuelaskpop@kpop.social']
xhighscore = 6
xpl_id = 'PLZyP4b181sFbU1gqOo84cuCW7TevM01Ql'


xpl_date = 'February 24, 2025'
xpl_hashtag = 'LettingGo'
xpl_toot_count = 30
xleaderboard = ['euphoricaster@apobangpo.space', 'abuelaskpop@kpop.social']
xhighscore = 5
xpl_id = 'PLZyP4b181sFbswHGCR-ph-0IfVzA2B4G8'

xpl_date = 'February 17, 2025'
xpl_hashtag = 'FaceCards'
xpl_toot_count = 20
xleaderboard = ['Erzbet@apobangpo.space']
xhighscore = 6
xpl_id = 'PLZyP4b181sFYm2j6Hr0RJhwl2X1b6QuPz'
# https://youtube.com/playlist?list=PLZyP4b181sFYm2j6Hr0RJhwl2X1b6QuPz&si=ip5ysJgETHFJmigX


xpl_date = 'February 10, 2025'
xpl_hashtag = 'BeepBeep'
xpl_toot_count = 49
xleaderboard = ['Erzbet@apobangpo.space', 'abuelaskpop@kpop.social']
xhighscore = 7
xpl_id = 'PLZyP4b181sFZKynQ0rnXNvg7dWhb05KAB'


xpl_date = 'February 03, 2025'
xpl_hashtag = 'BirthdayWishes'
xpl_toot_count = 21
xleaderboard = ['nikunashi@ieji.de', 'abuelaskpop@kpop.social', 'JillsJoy@nerdjoy.social']
xhighscore = 3
xpl_id = 'PLZyP4b181sFZoFwv7r6HIquhSQkM7L3I7'
# https://youtube.com/playlist?list=PLZyP4b181sFZoFwv7r6HIquhSQkM7L3I7&si=n-owClLJfkrB02Kc
'''

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