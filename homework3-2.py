"""
取得每部電影的全文介紹
"""

import requests
import re
import json
from bs4 import BeautifulSoup


Y_MOVIE_URL = 'https://tw.movies.yahoo.com/movie_thisweek.html'

# 以下網址後面加上 "/id=MOVIE_ID" 即為該影片各項資訊
Y_INTRO_URL = 'https://tw.movies.yahoo.com/movieinfo_main.html'  # 詳細資訊
Y_PHOTO_URL = 'https://tw.movies.yahoo.com/movieinfo_photos.html'  # 劇照
Y_TIME_URL = 'https://tw.movies.yahoo.com/movietime_result.html'  # 時刻表


def get_web_page(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text


def get_movies(dom):
    soup = BeautifulSoup(dom, 'html5lib')
    movies = []
    rows = soup.find_all('div', 'clearfix row')
    for row in rows:
        movie = dict()
        movie['expectation'] = row.find(id='ymvle').find('div', 'bd clearfix ').em.text
        movie['ch_name'] = row.find('div', 'text').h4.text
        movie['eng_name'] = row.find('div', 'text').h5.text
        movie['movie_id'] = get_movie_id(row.find('div', 'text').h4.a['href'])
        movie['poster_url'] = row.find('div', 'img').img['src'].replace('mpost4', 'mpost')
        movie['release_date'] = get_date(row.find('div', 'text').span.text)
        movie['intro'] = get_complete_intro(movie['movie_id'])
        trailer_li = row.find('div', 'text').find('li', 'trailer')
        movie['trailer_url'] = get_trailer_url(trailer_li.a['href']) if trailer_li else ''
        movies.append(movie)
    return movies


def get_date(date_str):
    # e.g. "上映日期：2017-03-23" -> match.group(0): "2017-03-23"
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, date_str)
    if match is None:
        return date_str
    else:
        return match.group(0)


def get_movie_id(url):
    # e.g. "https://tw.rd.yahoo.com/referurl/movie/thisweek/info/*https://tw.movies.yahoo.com/movieinfo_main.html/id=6707"
    #      -> match.group(0): "/id=6707"
    pattern = '/id=\d+'
    match = re.search(pattern, url)
    if match is None:
        return url
    else:
        return match.group(0).replace('/id=', '')


def get_trailer_url(url):
    # e.g., 'https://tw.rd.yahoo.com/referurl/movie/thisweek/trailer/*https://tw.movies.yahoo.com/video/美女與野獸-最終版預告-024340912.html'
    return url.split('*')[1]


def get_complete_intro(movie_id):
    page = get_web_page(Y_INTRO_URL + '/id=' + movie_id)
    if page:
        soup = BeautifulSoup(page, 'html5lib')

        div_text_full = soup.find('div', 'text full')
        return div_text_full
    return None  # 可能會有沒在 text full 的可能


def main():
    page = get_web_page(Y_MOVIE_URL)
    if page:
        movies = get_movies(page)
        for movie in movies:
            print(movie)
        with open('movie.json', 'w', encoding='utf-8') as f:
            json.dump(movies, f, indent=2, sort_keys=True, ensure_ascii=False)


if __name__ == '__main__':
    main()