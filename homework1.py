'''
- 取出範例網頁的標題 (title) 與段落 (p) 文字
- 讓程式試著取出範例網頁中不存在的標籤文字 (如 button.text), 並且在標籤不存在時, 程式能正常結束
'''

import requests
from bs4 import BeautifulSoup

def main():
    show_head_text('標題(title)', 'title')
    show_head_text('標籤p', 'p')
    show_head_text('不存在的 button.text', 'button.text')

def show_head_text(show_string, label):
    url = 'http://blog.castman.net/web-crawler-tutorial/ch1/connect.html'
    print(show_string + ': {}'.format(get_head_text(url, label)))

def get_head_text(url, head_tag):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            return soup.find(head_tag).text
    except Exception as e:
        return None

if __name__ == '__main__':
    main()
