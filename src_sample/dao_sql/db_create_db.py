# -*- coding: utf-8 -*-

import sqlite3

print('START')
# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = 'TWEET_DATA.sqlite'
conn = sqlite3.connect(dbname)

# データベースへのコネクションを閉じる。(必須)
conn.close()
print('END')