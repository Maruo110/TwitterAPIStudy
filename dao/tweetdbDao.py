# -*- coding: utf-8 -*-

def selectHashtagTbl(cur, hashtag_word):

    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()

    if result is None:
        return -1
    else:
        return  int(result[0])
    
"""
    if cur.rowcount < 0:
    #if len(cur.fetchall()) == 0:
        return -1
    else:
        hashtagid = cur.fetchone()
        return  hashtagid
"""

def insertHashTagTbl(conn, cur, hashtag_word):
    cur.execute("INSERT INTO t_hashtag(s_hashtagword) values('" + hashtag_word + "')")
    conn.commit()
    #conn.close()

    cur.execute("SELECT n_hashtagid FROM t_hashtag where s_hashtagword = '" + hashtag_word + "'")

    result = cur.fetchone()
    return  int(result[0])







