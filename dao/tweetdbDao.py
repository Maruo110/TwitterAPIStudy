# -*- coding: utf-8 -*-

def insertTrendTbl(conn, cur, insertValues):

    cur.execute("INSERT INTO t_trend(s_trendword, s_syutokuymd, s_syutokutime, n_tweetvolume, n_hashtagflg, n_hashtagid) values(" + insertValues + ")")
    conn.commit()


def getMaxIdTrendTbl(cur):

    cur.execute("SELECT max(n_trendid) FROM t_trend")

    result = cur.fetchone()
    return  int(result[0])


def insertTweetTbl(conn, cur, insertValues):

    cur.execute("INSERT INTO t_tweet(s_userid, s_tweettext, n_retweetvolume, n_favoritevolume, s_tweeturl, s_tweettime) values(" + insertValues + ")")
    conn.commit()


def getMaxIdTweetTbl(cur):

    cur.execute("SELECT max(n_tweetid) FROM t_tweet")

    result = cur.fetchone()
    return  int(result[0])


def insertTrendTweet(conn, cur, trend_id, tweet_id):

    cur.execute("INSERT INTO t_trendtweet(n_trendid, n_tweetid) values(" + str(trend_id) + ", " + str(tweet_id) + ")")
    conn.commit()


def getExistRecordByTrendTweet(cur, trend_id, tweet_id):

    cur.execute("SELECT count(n_trendid) FROM t_trendtweet where n_trendid = " + str(trend_id) + " and n_tweetid = " + str(tweet_id))

    result = cur.fetchone()

    if result is None:
        return False
    else:
        return True

def getHashTagId(cur, hashtag_word):

    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])


def insertHashTagTbl(conn, cur, hashtag_word):
    cur.execute("INSERT INTO t_hashtag(s_hashtagword) values('" + hashtag_word + "')")
    conn.commit()


def insertUrlTbl(conn, cur, url):
    cur.execute("INSERT INTO t_url(s_linkedurl) values('" + url + "')")
    conn.commit()


def getUrlId(cur, url):
    cur.execute("SELECT n_linkedurlid FROM t_url where s_linkedurl = '" + url + "'")

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])


def getMaxUrlId(cur):

    cur.execute("SELECT max(n_linkedurlid) FROM t_url")

    result = cur.fetchone()
    return  int(result[0])

def insertTweetUrl(conn, cur, tweet_id, url_id):

    cur.execute("INSERT INTO t_tweeturl(n_tweetid, n_linkedurlid) values(" + str(tweet_id) + ", " + str(url_id) + ")")
    conn.commit()

def getExistRecordByTweetUrl(cur, tweet_id, url_id):

    cur.execute("SELECT count(n_tweetid) FROM t_tweeturl where n_tweetid = " + str(tweet_id) + " and n_linkedurlid= " + str(url_id))

    result = cur.fetchone()

    if result is None:
        return False
    else:
        return True

def insertTweetHashtagTbl(conn, cur, tweet_id, hashtag_id):

    cur.execute("INSERT INTO t_tweethashtag(n_tweetid, n_hashtagid) values(" + str(tweet_id) + ", " + str(hashtag_id) + ")")
    conn.commit()


def getExistRecordByTweetHashtag(cur, tweet_id, hashtag_id):

    cur.execute("SELECT count(n_tweetid) FROM t_tweethashtag where n_tweetid = " + str(tweet_id) + " and n_hashtagid= " + str(hashtag_id))

    result = cur.fetchone()

    if result is None:
        return False
    else:
        return True


"""
def getHashTagId(cur, hashtag_word):
    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()
    return  int(result[0])
"""
