# -*- coding: utf-8 -*-

import json, config, worldid, sqlite3, datetime
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
from datetime import datetime
from dao import tweetdbDao

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

# APIエンドポイント（トレンド取得）
url = "https://api.twitter.com/1.1/trends/place.json"

# APIエンドポイント（ツイート取得＜拡張版＞）
url2 = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

params = {
    'id' : worldid.Japan
}

db_connection = sqlite3.connect(config.DB_NAME)
# sqliteを操作するカーソルオブジェクトを作成
db_cursol = db_connection.cursor()

date_today = datetime.now().strftime("%Y-%m-%d")
date_time = datetime.now().strftime("%H:%M:%S")

req = twitter.get(url, params = params)

if req.status_code == 200:
    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        trend_word = trendinfo['name']

        if len(trend_word) > 0:

            if trend_word[0] == '#':
                hashtag_flg = 1
                trend_word_id = tweetdbDao.selectHashtagTbl(db_cursol, trend_word)

                if trend_word_id < 0:
                    trend_word_id = tweetdbDao.insertHashTagTbl(db_connection, db_cursol, trend_word)

            else:
                hashtag_flg = 0
                trend_word_id = -1

        else:
            hashtag_flg = 0
            trend_word_id = -1

        trend_volume = trendinfo['tweet_volume']


        print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
        print('＞' + trend_word + '  [' + str(trend_volume) + ']')


        params2 = {
            'q' : trendinfo['name'],
            'lang' : 'ja',
            'result_type' : 'popular',
            'count' : 3
        }

        if trendinfo['tweet_volume'] is None:
            tweet_volume = "-1"

        else:
            tweet_volume = str(trendinfo['tweet_volume'])

        insert_values = "'" + trendinfo['name'] + "','" + str(date_today) + "','" + str(date_time) + "'"
        insert_values = insert_values + "," + tweet_volume
        insert_values = insert_values + "," + str(hashtag_flg)
        insert_values = insert_values + "," + str(trend_word_id)

        #print("insert_values＝" + insert_values)
        trendid = tweetdbDao.insertTrendTbl(db_connection, db_cursol, insert_values)


        req2 = twitter.get(url2, params = params2)

        if req2.status_code == 200:
            search_timeline = json.loads(req2.text)
            for tweet in search_timeline['statuses']:
                print('-----------------------------------------------------')
                print('@' + tweet['user']['screen_name'])
                print('＞' + tweet['user']['name'])
                print('＞' + tweet['created_at'])
                print('＞RT=' + str(tweet['retweet_count']) + '　＞FV=' + str(tweet['favorite_count']))
                print('＞' + tweet['full_text'])

                # ツイートURL
                tweet_url = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                print ('＞' + tweet_url)
                print('＞https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str'])

                # ハッシュタグ
                hashtaglist = tweet['entities']['hashtags']
                for hashtag in hashtaglist:
                    print('＞#' + hashtag['text'])

                # リンクURL
                link_url_list = tweet['entities']['urls']
                for link_url in link_url_list:
                    print('＞' + link_url['expanded_url'])


                tweet_insert_value = "'@" + tweet['user']['screen_name'] + "'"
                tweet_insert_value = tweet_insert_value + ", '" + tweet['full_text'] + "'"
                tweet_insert_value = tweet_insert_value + ", " + str(tweet['retweet_count'])
                tweet_insert_value = tweet_insert_value + ", " + str(tweet['favorite_count'])
                tweet_insert_value = tweet_insert_value + ", '" + tweet_url + "'"
                tweet_insert_value = tweet_insert_value + ", '" + tweet['created_at'] + "'"
                print ("tweet_insert_value＝" + tweet_insert_value)

                tweet_id = tweetdbDao.insertTweetTbl(db_connection, db_cursol, tweet_insert_value)
                print ('tweet_id＝' + str(tweet_id))

                tweetdbDao.insertTrendTweet(db_connection, db_cursol, trendid, tweet_id)

                print('-----------------------------------------------------')

        else:
            print("ERROR: %d" % req2.status_code)

        print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')

else:
    print("ERROR: %d" % req.status_code)


# データベースへコミット。これで変更が反映される。
db_connection.commit()
db_connection.close()




