# -*- coding: utf-8 -*-


def getWebInfoKihon():
    import requests

    #get_url_info = requests.get('https://www.python.org/')
    #print(get_url_info)

    get_url_info = requests.get('https://news.yahoo.co.jp/pickup/6357692')

    # コンテンツタイプの取得
    print(get_url_info.headers['content-type']) #=>text/html
    print('--------------------------------------------------')

    # エンコーディング情報
    print(get_url_info.encoding) #=>ISO-8859-1
    print('--------------------------------------------------')

    # web ページの中身
    print(get_url_info.text) #=> <!DOCTYPE html>...</html>
    print('--------------------------------------------------')



if __name__ == '__main__':
    getWebInfoKihon()

