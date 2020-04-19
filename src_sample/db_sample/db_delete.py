# -*- coding: utf-8 -*-

import sqlite3

dbname = 'TWEET_DATA.sqlite'
conn = sqlite3.connect(dbname)
# sqliteを操作するカーソルオブジェクトを作成
cur = conn.cursor()

# Insert a row of data
#cur.execute("INSERT INTO persons(name) values('Mike')")

# Delete data
cur.execute("DELETE FROM persons WHERE name = 'Mike'")

# データベースへコミット。これで変更が反映される。
conn.commit()
conn.close()
