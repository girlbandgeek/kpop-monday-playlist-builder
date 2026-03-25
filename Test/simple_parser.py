# Simplified Test script to test parsing logic

import re


# ccontent = hashtag_dict[key]["content"]

my_content = ['The cat is in the bed.', 'The dog is in the dog house.', 'The fish is in its bowl', 'The moon is a balloon.']

for ccontent in my_content:
    print(ccontent)
    print('')



    wordPattern = '|'.join([
	r'dog',
	r'cat',
	r'fish'
	])

    print(wordPattern)

    pattern = re.compile(wordPattern)
    print(pattern)

    match = pattern.findall(ccontent)

    if len(match) > 0:
        print(f"words: ", match)
        vid_list=[]
        for iitem in match:
            vid_list.append(iitem[1])
        # remove duplicate videos
        new_vid_list = list(set(vid_list))
        print("words: ", new_vid_list)
        print('')
        # rlist.append(new_vid_list)
    else:
        print(f"words: NOT MATCHED!!!")
        print('')
        # rlist.append([])
