# -*- coding: utf-8 -*-

import json, config, worldid, sqlite3, datetime
from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み

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


req = twitter.get(url, params = params)

if req.status_code == 200:
    search_trend = json.loads(req.text)

    for trendinfo in search_trend[0]['trends']:
        print('▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
        print('＞' + trendinfo['name'] + '  [' + str(trendinfo['tweet_volume']) + ']')

        params2 = {
            'q' : trendinfo['name'],
            'lang' : 'ja',
            'result_type' : 'popular',
            'count' : 3
        }

        if trendinfo['tweet_volume'] is None:
            tweet_volume = "-1"
            #insert_values = "'" + trendinfo['name'] + "',-1"
            #insert_values = "'" + trendinfo['name'] + "'," + str(datetime.date.today()) + ",-1"

        else:
            tweet_volume = str(trendinfo['tweet_volume'])
            #insert_values = "'" + trendinfo['name'] + "'," + str(trendinfo['tweet_volume'])

        insert_values = "'" + trendinfo['name'] + "','" + str(datetime.date.today()) + "'"
        insert_values = insert_values + "," + tweet_volume

        #db_cursol.execute("INSERT INTO t_trend(s_trendword,s_syutokuymd,s_syutokutime,n_tweetvolume) values()")
        #db_cursol.execute("INSERT INTO t_trend(s_trendword,n_tweetvolume) values(" + insert_values + ")")
        db_cursol.execute("INSERT INTO t_trend(s_trendword,s_syutokuymd,n_tweetvolume) values(" + insert_values + ")")

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
                print('＞https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str'])

                # ハッシュタグ
                hashtaglist = tweet['entities']['hashtags']
                for hashtag in hashtaglist:
                    print('＞#' + hashtag['text'])

                # リンクURL
                link_url_list = tweet['entities']['urls']
                for link_url in link_url_list:
                    print('＞' + link_url['expanded_url'])

                print('-----------------------------------------------------')

        else:
            print("ERROR: %d" % req2.status_code)

        print('▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')

else:
    print("ERROR: %d" % req.status_code)


# データベースへコミット。これで変更が反映される。
db_connection.commit()
db_connection.close()
