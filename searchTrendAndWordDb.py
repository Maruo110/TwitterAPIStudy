# -*- coding: utf-8 -*-
import time
import threading

def run_searchTrendInfo():

    import json, sqlite3, datetime, logging.config, requests, re
    from config import worldid
    from config import app_config
    from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
    from datetime import datetime
    from dao import tweetdbDao
    from google_cloud_api import natural_language
    from util import utils
    from logging import getLogger
    from bs4 import BeautifulSoup

    logging.config.fileConfig('logging.conf')
    logger = getLogger()
    logger.info('▼▼▼▼▼▼START▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼')
    date_today = datetime.now().strftime("%Y-%m-%d")
    date_time = datetime.now().strftime("%H:%M:%S")

    logger.info('｜処理日: %s', date_today)
    logger.info('｜処理時間: %s', date_time)

    CK = app_config.CONSUMER_KEY
    CS = app_config.CONSUMER_SECRET
    AT = app_config.ACCESS_TOKEN
    ATS = app_config.ACCESS_TOKEN_SECRET
    twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

    # APIエンドポイント（トレンド取得）
    url = "https://api.twitter.com/1.1/trends/place.json"
    # APIエンドポイント（ツイート取得＜拡張版＞）
    url2 = "https://api.twitter.com/1.1/search/tweets.json?tweet_mode=extended"

    params = {'id' : worldid.Japan}

    req = twitter.get(url, params = params)

    count_trend     = 0
    count_tweet     = 0
    count_hashtag   = 0
    count_linkedurl = 0

    db_connection = sqlite3.connect(app_config.DB_NAME)
    db_cursol = db_connection.cursor()

    if req.status_code == 200:
        logger.debug('｜◇Twitter OAuth認証通過')

        search_trend = json.loads(req.text)

        for trendinfo in search_trend[0]['trends']:
            count_trend += 1
            trend_word = trendinfo['name']

            hashtag_flg = 0
            trend_word_id = -1
            trend_sentiment_score = 0.0
            trend_linked_tweet_cnt = 0

            if trend_word[0] == '#':
                hashtag_flg = 1
                trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)

                if trend_word_id < 0:
                    tweetdbDao.insertHashTagTbl(db_connection, db_cursol, trend_word)
                    trend_word_id = tweetdbDao.getHashTagId(db_cursol, trend_word)
            else:
                pass

            logger.debug('｜▽trend_word: %s', trend_word)

            trend_volume = trendinfo['tweet_volume']

            if trend_volume is None:
                tweet_volume = "-1"

            else:
                tweet_volume = str(trend_volume)

            insert_values = "'" + trend_word + "','" + str(date_today) + "','" + str(date_time) + "'"
            insert_values = insert_values + "," + tweet_volume
            insert_values = insert_values + "," + str(hashtag_flg)
            insert_values = insert_values + "," + str(trend_word_id)

            #print("insert_values＝" + insert_values)
            tweetdbDao.insertTrendTbl(db_connection, db_cursol, insert_values)
            trendid = tweetdbDao.getMaxIdTrendTbl(db_cursol)

            params2 = {
                'q' : trend_word,
                'lang' : 'ja',
                'result_type' : 'popular',
                'count' : app_config.GET_TWEET_CNT
            }

            req2 = twitter.get(url2, params = params2)

            if req2.status_code == 200:
                search_timeline = json.loads(req2.text)

                for tweet in search_timeline['statuses']:
                    count_tweet += 1
                    trend_linked_tweet_cnt += 1

                    logger.debug('｜｜▽tweet')

                    tweet_datetime = utils.convert_datetime(tweet['created_at'])
                    tweet_url = 'https://twitter.com/' + tweet['user']['screen_name'] + '/status/' + tweet['id_str']
                    tweet_text = utils.removeSingleCotation(tweet['full_text'])
                    tweet_text = utils.removeEmojiStr(tweet_text)
                    tweet_text_for_gcp = utils.removeUrlLinkStr(tweet_text)

                    # GCP実行
                    tweet_sentiment = natural_language.getSentiment(tweet_text_for_gcp)
                    tweet_sentiment_score     = '{:.02f}'.format(tweet_sentiment.score)
                    tweet_sentiment_magnitude = '{:.05f}'.format(tweet_sentiment.magnitude)
                    tweet_valid_str_count = len(tweet_text_for_gcp)

                    trend_sentiment_score = trend_sentiment_score + float(tweet_sentiment_score)

                    #logger.debug('｜｜｜tweet_text_for_gcp :%s', tweet_text_for_gcp)
                    logger.debug('｜｜｜tweet_sentiment_score :%s', tweet_sentiment_score)

                    tweet_insert_value = "'@" + tweet['user']['screen_name'] + "'"
                    tweet_insert_value = tweet_insert_value + ", '" + tweet_text + "'"
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet['retweet_count'])
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet['favorite_count'])
                    tweet_insert_value = tweet_insert_value + ", '" + tweet_url + "'"
                    tweet_insert_value = tweet_insert_value + ", '" + str(tweet_datetime) + "'"
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_sentiment_score)
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_sentiment_magnitude)
                    tweet_insert_value = tweet_insert_value + ", "  + str(tweet_valid_str_count)

                    #print ("tweet_insert_value＝" + tweet_insert_value)

                    tweetdbDao.insertTweetTbl(db_connection, db_cursol, tweet_insert_value)
                    tweet_id = tweetdbDao.getMaxIdTweetTbl(db_cursol)

                    logger.debug('｜｜｜tweet_id: %s, tweet_url: %s', str(tweet_id), tweet_url)

                    if tweetdbDao.getExistRecordByTrendTweet(db_cursol, trendid, tweet_id) == False:
                        tweetdbDao.insertTrendTweet(db_connection, db_cursol, trendid, tweet_id)
                    else:
                        pass

                    # ハッシュタグ
                    hashtaglist = tweet['entities']['hashtags']

                    for hashtag in hashtaglist:
                        count_hashtag += 1
                        tweet_hashtag = hashtag['text']

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

                    # リンクURL
                    link_url_list = tweet['entities']['urls']

                    for link_url in link_url_list:
                        count_linkedurl += 1
                        url = link_url['expanded_url']

                        url_id = tweetdbDao.getUrlId(db_cursol, url)

                        if url_id < 0:
                            tweetdbDao.insertUrlTbl(db_connection, db_cursol, url)
                            url_id = tweetdbDao.getMaxUrlId(db_cursol)

                            # スクレイピング
                            web_res = requests.get(url).text
                            web_soup = BeautifulSoup(web_res, 'html.parser')
                            ptag = web_soup.find_all("p")
                            ptag_value = ""

                            for p in ptag:
                                ptag_value = ptag_value + '\n' + utils.removeSingleCotation(p.text)
                                #print(p.text)

                            ptag_value = re.sub('[\r\n]+$', '', ptag_value)


                            logger.debug('｜｜｜スクレイピング')
                            logger.debug('｜｜｜ptag_value: %s', ptag_value)

                        else:
                            pass

                        if tweetdbDao.getExistRecordByTweetUrl(db_cursol, tweet_id, url_id) == False:
                            tweetdbDao.insertTweetUrl(db_connection, db_cursol, tweet_id, url_id)
                        else:
                            pass

                    logger.debug('｜｜△')

                # トレンド情報にGCP結果を更新
                if trend_linked_tweet_cnt <= 0:
                    ave_tweet_sentiment_score = 0
                else:
                    ave_tweet_sentiment_score = trend_sentiment_score/trend_linked_tweet_cnt

                tweetdbDao.updateTrendTblGcpResult(db_connection, db_cursol, trendid, ave_tweet_sentiment_score)

                logger.debug('｜△')

            else:
                logger.debug('｜!ERR! StatusCode: %s', req2.status_code)
                logger.debug('｜△')

    else:
        logger.debug('｜◇Twitter OAuth認証≪失敗≫')
        logger.debug('｜!ERR! StatusCode: %s', req.status_code)

    logger.info('｜トレンド情報登録[正常終了]')

    db_connection.commit()
    db_connection.close()

    logger.info('｜count_trend    : %d'    , count_trend)
    logger.info('｜count_tweet    : %d'    , count_tweet)
    logger.info('｜count_hashtag  : %d'  , count_hashtag)
    logger.info('｜count_linkedurl: %d', count_linkedurl)
    logger.info('▲▲▲▲▲▲END▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲')


if __name__ == '__main__':
    run_searchTrendInfo()


"""
def schedule(interval, f, wait=True):
    base_time = time.time()
    next_time = 0
    while True:
        t = threading.Thread(target=f)
        t.start()
        if wait:
            t.join()
        next_time = ((base_time - time.time()) % interval) or interval
        time.sleep(next_time)


if __name__ == '__main__':
    schedule(300, run_searchTrendInfo)
    #run_searchTrendInfo()
"""
