# -*- coding: utf-8 -*-


def getWebInfoBeautifulSoup4():

    import requests
    from bs4 import BeautifulSoup
    from util import utils

    url = "https://news.line.me/articles/oa-rp73073/9ea6e70c0e15"
    res = requests.get(url).text

    soup = BeautifulSoup(res, 'html.parser') #2
    ptag = soup.find_all("title")
    ptag_value = ""

    print ("@" + ptag[0].text)

    for p in ptag:
        ptag_value = ptag_value + p.text

    ptag_value = utils.removeKaigyou(ptag_value)
    print(ptag_value)
    print('--------------------------------------------------')

if __name__ == '__main__':
    getWebInfoBeautifulSoup4()

