# Test script to test parsing logic

import re


# ccontent = hashtag_dict[key]["content"]
my_content = ['<p>I love when kpop does Spanish, and this one is one of my absolute favs</p><p>Demente - Chungha</p><p><a href="https://www.youtube.com/watch?si=6EQBevEEr1S_H7EH&amp;v=KsHZI6nYLFM" rel="nofollow noopener" translate="no" target="_blank"><span class="invisible">https://www.</span><span class="ellipsis">youtube.com/watch?si=6EQBevEEr</span><span class="invisible">1S_H7EH&amp;v=KsHZI6nYLFM</span></a></p><p><a href="https://kpop.social/tags/KpopMonday" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>KpopMonday</span></a> <a href="https://kpop.social/tags/NonKoreanReleases" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>NonKoreanReleases</span></a> <a href="https://kpop.social/tags/kpop" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>kpop</span></a> <a href="https://kpop.social/tags/Chungha" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>Chungha</span></a></p>', '<p><a href="https://borahae.love/tags/nonkoreanreleases" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>nonkoreanreleases</span></a> <a href="https://borahae.love/tags/kpopmonday" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>kpopmonday</span></a> </p><p>No official video, but <a href="https://borahae.love/tags/BTS" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>BTS</span></a> <a href="https://borahae.love/tags/dontleaveme" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>dontleaveme</span></a> from Japanese album <a href="https://borahae.love/tags/FaceYourself" class="mention hashtag" rel="nofollow noopener" target="_blank">#<span>FaceYourself</span></a></p><p><a href="https://youtu.be/8Fzc14ftwN4?si=JOrVdauQRWVFo8r0" rel="nofollow noopener" translate="no" target="_blank"><span class="invisible">https://</span><span class="ellipsis">youtu.be/8Fzc14ftwN4?si=JOrVda</span><span class="invisible">uQRWVFo8r0</span></a></p>']

for ccontent in my_content:
    # match = re.findall(r'(m\.youtube\.com/watch\?v=|www\.youtube\.com/watch\?v=|www\.youtube\.com/v/|youtu\.be/)([\w-]+)', ccontent)
    # match = re.findall(r'(m\.youtube\.com/watch\?v=|www\.youtube\.com/watch\?v=|www\.youtube\.com/v/|youtu\.be/|www\.youtube\.com/watch\?si=)([\w-]+)', ccontent)

    # Note: above expression is working. Below, trying to work out how to put regex
    # on multiple lines for clarity. Currently not working :()

#    pattern = re.compile(r"""(\
#        m\.youtube\.com/watch\?v=\
#        |www\.youtube\.com/watch\?v=\
#        |www\.youtube\.com/v/\
#        |youtu\.be/|www\.youtube\.com/watch\?si=)\
#        ([\w-]+)""")

#    pattern = re.compile(r"""(m\.youtube\.com/watch\?v=
#                              |www\.youtube\.com/watch\?v=
#                              |www\.youtube\.com/v/
#                              |youtu\.be/|www\.youtube\.com/watch\?si=)([\w-]+)""")

    videoPattern = '|'.join([
	# Normal watch URL   :: r'[0-9A-Za-z_-]{11}',
	r'/www\.youtube\.com/watch(_popup)?(\.php)?/?\?(\S*&)?v=[0-9A-Za-z_-]{11}',
	r'm\.youtube\.com/watch\?v=[0-9A-Za-z_-]{11}',
	r'www\.youtube\.com/watch\?v=[0-9A-Za-z_-]{11}',
	r'www\.youtube\.com/v/[0-9A-Za-z_-]{11}',
	r'youtu\.be/[0-9A-Za-z_-]{11}',
	r'www\.youtube\.com/watch\?si=[0-9A-Za-z_-]{11}'
	])

    pattern = re.compile(videoPattern)

    match = pattern.findall(ccontent)

    if len(match) > 0:
        print(f"videos: ", match)
        vid_list=[]
        for iitem in match:
            vid_list.append(iitem[1])
        # remove duplicate videos
        new_vid_list = list(set(vid_list))
        print("video ID's: ", new_vid_list)
        # rlist.append(new_vid_list)
    else:
        print(f"videos: NOT MATCHED!!!")
        # rlist.append([])
