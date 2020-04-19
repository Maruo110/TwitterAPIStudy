# -*- coding: utf-8 -*-

import json, worldid, sqlite3, datetime, logging.config
import app_pconfig
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from datetime import datetime
from dao import tweetdbDao
from util import utils
from logging import getLogger

LOG_LEVEL_DEBUG = 10

# ログ設定ファイルからログ設定を読み込み
logging.config.fileConfig('logging.conf')
logger = getLogger()
logger.info('▼▼▼▼▼▼START▼▼▼▼▼▼')
date_today = datetime.now().strftime("%Y-%m-%d")
date_time = datetime.now().strftime("%H:%M:%S")

logger.info('｜処理日: %s', date_today)
logger.info('｜処理時間: %s', date_time)


CK = app_pconfig.CONSUMER_KEY
CS = app_pconfig.CONSUMER_SECRET
AT = app_pconfig.ACCESS_TOKEN
ATS = app_pconfig.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# APIエンドポイント（トレンド取得）
url = "https://api.twitter.com/1.1/trends/place.json"

# APIエンドポイント（ツイート取得＜拡張版＞）
url2 = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

params = {
    'id' : worldid.Japan
}

db_connection = sqlite3.connect(app_pconfig.DB_NAME)
# sqliteを操作するカーソルオブジェクトを作成
db_cursol = db_connection.cursor()

req = twitter.get(url, params = params)

if req.status_code == 200:
    logger.debug('｜◇Twitter OAuth認証通過')

    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        trend_word = trendinfo['name']

        hashtag_flg = 0
        trend_word_id = -1

        if len(trend_word) > 0:

            if trend_word[0] == '#':
                hashtag_flg = 1
                trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)

                if trend_word_id < 0:
                    tweetdbDao.insertHashTagTbl(db_connection, db_cursol, trend_word)
                    trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)
            else:
                pass

        else:
            pass

        logger.debug('｜▽trend_word: %s', trend_word)

        params2 = {
            'q' : trend_word,
            'lang' : 'ja',
            'result_type' : 'popular',
            'count' : 2
        }

        trend_volume = trendinfo['tweet_volume']

        if trend_volume is None:
            tweet_volume = "-1"

        else:
            tweet_volume = str(trendinfo['tweet_volume'])

        insert_values = "'" + trend_word + "','" + str(date_today) + "','" + str(date_time) + "'"
        insert_values = insert_values + "," + tweet_volume
        insert_values = insert_values + "," + str(hashtag_flg)
        insert_values = insert_values + "," + str(trend_word_id)

        #print("insert_values＝" + insert_values)
        tweetdbDao.insertTrendTbl(db_connection, db_cursol, insert_values)
        trendid = tweetdbDao.getMaxIdTrendTbl(db_cursol)

        req2 = twitter.get(url2, params = params2)

        if req2.status_code == 200:
            search_timeline = json.loads(req2.text)
            for tweet in search_timeline['statuses']:

                logger.debug('｜｜▽tweet')
                tweet_datetime = utils.convert_datetime(tweet['created_at'])

                print('-----------------------------------------------------')
                print('@' + tweet['user']['screen_name'])
                print('＞' + tweet['user']['name'])
                print('＞' + str(tweet_datetime))
                print('＞RT=' + str(tweet['retweet_count']) + '　＞FV=' + str(tweet['favorite_count']))
                print('＞' + tweet['full_text'])

                # ツイートURL
                tweet_url = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                print ('＞' + tweet_url)
                print('＞https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str'])

                tweet_insert_value = "'@" + tweet['user']['screen_name'] + "'"
                tweet_insert_value = tweet_insert_value + ", '" + tweet['full_text'] + "'"
                tweet_insert_value = tweet_insert_value + ", " + str(tweet['retweet_count'])
                tweet_insert_value = tweet_insert_value + ", " + str(tweet['favorite_count'])
                tweet_insert_value = tweet_insert_value + ", '" + tweet_url + "'"
                tweet_insert_value = tweet_insert_value + ", '" + str(tweet_datetime) + "'"
                print ("tweet_insert_value＝" + tweet_insert_value)

                tweetdbDao.insertTweetTbl(db_connection, db_cursol, tweet_insert_value)
                tweet_id = tweetdbDao.getMaxIdTweetTbl(db_cursol)
                print ('tweet_id＝' + str(tweet_id))

                if tweetdbDao.getExistRecordByTrendTweet(db_cursol, trendid, tweet_id) == False:
                    tweetdbDao.insertTrendTweet(db_connection, db_cursol, trendid, tweet_id)
                else:
                    pass

                # ハッシュタグ
                hashtaglist = tweet['entities']['hashtags']
                for hashtag in hashtaglist:

                    tweet_hashtag = hashtag['text']
                    print('＞#' + tweet_hashtag)

                    tweet_hashtagid = tweetdbDao.getHashTagId(db_cursol, tweet_hashtag)

                    if tweet_hashtagid < 0:
                        tweetdbDao.insertHashTagTbl(db_connection, db_cursol, tweet_hashtag)
                        tweet_hashtagid = tweetdbDao.getHashTagId(db_cursol, tweet_hashtag)
                    else:
                        pass

                    if tweetdbDao.getExistRecordByTweetHashtag(db_cursol, tweet_id, tweet_hashtagid) == False:
                        tweetdbDao.insertTweetHashtagTbl(db_connection, db_cursol, tweet_id, tweet_hashtagid)
                    else:
                        pass

                # リンクURLoo
                link_url_list = tweet['entities']['urls']
                for link_url in link_url_list:
                    url = link_url['expanded_url']
                    print('＞' + url)

                    url_id = tweetdbDao.getUrlId(db_cursol, url)

                    if url_id < 0:
                        tweetdbDao.insertUrlTbl(db_connection, db_cursol, url)
                        url_id = tweetdbDao.getMaxUrlId(db_cursol)
                    else:
                        pass

                    if tweetdbDao.getExistRecordByTweetUrl(db_cursol, tweet_id, url_id) == False:
                        tweetdbDao.insertTweetUrl(db_connection, db_cursol, tweet_id, url_id)
                    else:
                        pass

                logger.debug('｜｜△')
            logger.debug('｜△')

        else:
            print("ERROR: %d" % req2.status_code)

        print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')

else:
    logger.log(LOG_LEVEL_DEBUG, '◇Twitter OAuth認証≪失敗≫')
    logger.log(LOG_LEVEL_DEBUG, '◇エラーコード＝' + req.status_code)

    print("ERROR: %d" % req.status_code)


# データベースへコミット。これで変更が反映される。
db_connection.commit()
db_connection.close()


logger.log(LOG_LEVEL_DEBUG, '▲▲▲▲▲▲END▲▲▲▲▲▲')

