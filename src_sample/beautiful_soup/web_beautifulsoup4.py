# -*- coding: utf-8 -*-


def getWebInfoBeautifulSoup4():

    import requests
    from bs4 import BeautifulSoup

    url = "https://news.yahoo.co.jp/byline/fujitatakanori/20200420-00174220/"
    res = requests.get(url).text

    soup = BeautifulSoup(res, 'html.parser') #2
    #print (soup)
    #print(soup.prettify())
    ptag = soup.find_all("p")
    #print(soup.find_all("p"))

    for p in ptag:
        #print(type(p))
        print(p.text)

    print('--------------------------------------------------')

if __name__ == '__main__':
    getWebInfoBeautifulSoup4()

