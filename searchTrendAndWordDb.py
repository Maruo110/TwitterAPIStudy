# -*- coding: utf-8 -*-
import time
import threading
from google_cloud_api.analyze_entities import getAnalizeEntityResult

def run_searchTrendInfo():

    import json, sqlite3, datetime, logging.config, requests
    from config import worldid
    from config import app_config
    from requests_oauthlib import OAuth1Session #OAuthのライブラリの読み込み
    from datetime import datetime
    from dao import tweetdbDao
    from google_cloud_api import natural_language, analyze_entities
    from google.cloud.language_v1 import enums
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

    params = {'id' : worldid.Japan, 'exclude': 'hashtags'}

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
            trend_word = trendinfo['name']
            trend_volume = trendinfo['tweet_volume']

            logger.debug('｜▽trend_word: %s', trend_word)

            if trend_volume is None:
                tweet_volume = "-1"
            else:
                tweet_volume = str(trend_volume)

            hashtag_flg = 0
            trend_word_id = -1
            trend_sentiment_score = 0.0
            trend_linked_tweet_cnt = 0

            tweetdbDao.insertTrendTbl(db_connection,
                                      db_cursol,
                                      date_today,
                                      date_time,
                                      tweet_volume,
                                      -1,
                                      trend_word)

            trend_id = tweetdbDao.getMaxIdByTrendTbl(db_cursol)

            count_trend += 1

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
                    tweet_text = removeNoise(tweet['full_text'])

                    # GCP実行
                    logger.debug('｜｜｜[GCP]tweet_text: %s, ', tweet_text)
                    tweet_sentiment = natural_language.getSentiment(tweet_text)

                    if tweet_sentiment is None:
                        tweet_sentiment_score     = 0.0
                        tweet_sentiment_magnitude = 0.0
                    else:
                        tweet_sentiment_score     = '{:.02f}'.format(tweet_sentiment.score)
                        tweet_sentiment_magnitude = '{:.05f}'.format(tweet_sentiment.magnitude)

                    tweet_valid_str_count = len(tweet_text)

                    trend_sentiment_score = trend_sentiment_score + float(tweet_sentiment_score)

                    logger.debug('｜｜｜tweet_sentiment_score :%s', tweet_sentiment_score)

                    tweet_userid ="@" + tweet['user']['screen_name']

                    tweetdbDao.insertTweetTbl(db_connection,
                                              db_cursol,
                                              tweet_userid,
                                              tweet['retweet_count'],
                                              tweet['favorite_count'],
                                              tweet_url,
                                              tweet_datetime,
                                              tweet_sentiment_score,
                                              tweet_sentiment_magnitude,
                                              tweet_valid_str_count,
                                              trend_id,
                                              -1,
                                              tweet_text)

                    tweet_id = tweetdbDao.getMaxIdByTweetTbl(db_cursol)

                    # リンクURL
                    link_url_list = tweet['entities']['urls']

                    for link_url in link_url_list:

                        url = link_url['expanded_url']

                        url_id = tweetdbDao.getUrlIdByUrlTbl(db_cursol, url)

                        if url_id < 0:

                            html = requests.get(url)
                            html.encoding = html.apparent_encoding
                            web_soup = BeautifulSoup(html.text, "html.parser")

                            ptag = web_soup.find_all("p")
                            url_title = web_soup.find_all("title")
                            ptag_value = ""
                            url_title_value = ""

                            for p in ptag:
                                ptag_value = ptag_value + '　' + p.text

                            for ptitle in url_title:
                                url_title_value = url_title_value + '　' + ptitle.text

                            ptag_value = removeNoise(ptag_value)
                            url_title_value = removeNoise(url_title_value)

                            # GCP実行
                            logger.debug('｜｜｜[GCP]ptag_value: %s, ', ptag_value)
                            ulr_sentiment = natural_language.getSentiment(ptag_value)
                            ulr_sentiment_score     = '{:.02f}'.format(ulr_sentiment.score)
                            ulr_sentiment_magnitude = '{:.05f}'.format(ulr_sentiment.magnitude)
                            ulr_valid_str_count = len(ptag_value)

                            tweetdbDao.insertUrlTbl(db_connection,
                                                    db_cursol,
                                                    url,
                                                    ulr_sentiment_score,
                                                    ulr_sentiment_magnitude,
                                                    ulr_valid_str_count,
                                                    url_title_value,
                                                    ptag_value)

                            url_id = tweetdbDao.getMaxIdByUrlTbl(db_cursol)
                            count_linkedurl += 1

                        else:
                            tweetdbDao.updateTweetTblUrlId(db_connection,
                               db_cursol,
                               tweet_id,
                               url_id)

                    logger.debug('｜｜△')

                # トレンド情報にGCP結果を更新
                if trend_linked_tweet_cnt <= 0:
                    ave_tweet_sentiment_score = 0
                else:
                    ave_tweet_sentiment_score = trend_sentiment_score/trend_linked_tweet_cnt

                tweetdbDao.updateTrendTblGcpResult(db_connection,
                                                   db_cursol,
                                                   trend_id,
                                                   ave_tweet_sentiment_score)
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


def removeNoise(str):
    from util import utils

    result_str = str
    result_str = utils.removeSingleCotation(result_str)
    result_str = utils.removeEmojiStr(result_str)
    result_str = utils.removeUrlLinkStr(result_str)
    result_str = utils.removeHashTagStr(result_str)
    result_str = utils.removeHashTag2Str(result_str)
    result_str = utils.removeMensyonStr(result_str)
    result_str = utils.removeKaigyou(result_str)
    result_str = utils.removeTabStr(result_str)
    result_str = utils.removeSpacesStr(result_str)

    return result_str


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
