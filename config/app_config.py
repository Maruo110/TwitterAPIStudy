# -*- coding: utf-8 -*-

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# 環境変数の値をAPに代入
CONSUMER_KEY        = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET     = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN        = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")

# データベース名
DB_NAME = "TWEET_DATA.sqlite"

# トレンド単位ツイート取得数
GET_TWEET_CNT = 3

