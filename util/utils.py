# -*- coding: utf-8 -*-

import sys
import time
import datetime

def convert_datetime(datetime_str):
  tweet_time = time.strptime(datetime_str,'%a %b %d %H:%M:%S +0000 %Y')
  tweet_datetime = datetime.datetime(*tweet_time[:6])
  return(tweet_datetime)


def removeSingleCotation(str):
    return str.replace("'", " @SingleCotation@")

"""
def removeNotBMPStr(str):
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), '')
    print(str.translate(non_bmp_map))
    return str.translate(non_bmp_map)
"""

def removeEmojiStr(str):
    import emoji
    return ''.join(c for c in str if c not in emoji.UNICODE_EMOJI)

def removeUrlLinkStr(str):
    import re
    return re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", str)

def removeHashTagStr(str):
    import re
    return re.sub(r"#(\w+)", "", str)

def removeKaigyou(str):
    #import re
    #return re.sub('[\r\n]+$', '', str)
    #return  str.strip()
    return '　'.join(str.splitlines())

if __name__ == '__main__':
    str = 'よい夫婦の日だそうで。#吉田鋼太郎 #瀬奈じゅん #今日俺劇場版 #今日から俺は︎  '
    print(str)
    print(removeHashTagStr(str))
