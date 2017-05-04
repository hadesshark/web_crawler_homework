'''
- 找出範例網頁一 總共有幾篇 blog 貼文
- 找出範例網頁一 總共有幾張圖片網址含有 'crawler' 字串
- 找出範例網頁二 總共有幾堂課程
- 用 Chrome 開發者工具, 找出 Dcard 的今日熱門文章區塊, 然後取得前十篇熱門文章的標題
(提示: 每一篇熱門文章都是 class 為 PostEntry_container_
開頭的 div, 可以用 find_all() 加上 regular expression 找出來; 標題文字被 <strong> 包圍)
'''

import requests
from bs4 import BeautifulSoup
import re

def main():
    url1 = 'http://blog.castman.net/web-crawler-tutorial/ch2/blog/blog.html'
    soup1 = sucess_soup(url1)

    card_blog = len(soup1.find_all('div', 'card-blog'))
    print('總共有{}篇 blog 貼文。'.format(card_blog))

    card_images = soup1.find_all('img', 'img-raised')
    have_crawler = [item for item in card_images if 'crawler' in item['src']]
    print('總共有{}張圖片網址含有 \'crawler\' 字串。'.format(len(have_crawler)))


    url2 = 'http://blog.castman.net/web-crawler-tutorial/ch2/table/table.html'
    soup = sucess_soup(url2)

    total_class = len(soup.find('table', 'table').tbody.find_all('tr'))
    print('總共有{}堂課程。'.format(total_class))


    url3 = 'https://www.dcard.tw/f'
    soup3 = sucess_soup(url3)
    dcard_title = soup3.find_all('strong', re.compile('PostEntry_title_'))
    print('Dcard 熱門前十文章標題：')
    for index, item in enumerate(dcard_title[:10]):
        print("{0:2d}. {1}".format(index + 1, item.text.strip()))


def sucess_soup(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        return None

if __name__ == '__main__':
    main()
