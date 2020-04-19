# -*- coding: utf-8 -*-

import time
import datetime

def convert_datetime(datetime_str):
  tweet_time = time.strptime(datetime_str,'%a %b %d %H:%M:%S +0000 %Y')
  tweet_datetime = datetime.datetime(*tweet_time[:6])
  return(tweet_datetime)


def removeSingleCotation(str):
    return str.replace("'", " @SingleCotation@")
