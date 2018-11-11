
import requests
import os
import random
import time
import re
from bs4 import BeautifulSoup

from proxy.proxy_getter import get_viable_proxy_list
from proxy.proxy_getter import get_html_proxy

from atomicenergy.c_func import get_html_txt, write_to_file

def crawler():
    # главный URL
    main_url = 'http://www.atomic-energy.ru'

    # получение всех прокси и заголовков
    list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'),10)
    cur_dir = os.path.dirname(__file__)
    useragent_filename = os.path.join(cur_dir, '../proxy/useragents.txt')
    list_of_user_agents = open(useragent_filename).read().split('\n')

    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    # Получаем ссылки с главной страницы
    text = get_html_txt(main_url,useragent, proxy)
    soup = BeautifulSoup(text, "html.parser")
    li = soup.find('nav').find('ul').find_all('li')
    urls = []
    for i in li:
        href = i.find('a', href = True)['href']
        if 'www' in href or ':' in href:
            continue
        href = main_url + href
        if href not in urls:
            urls.append(href)
    print(urls)
    # записываем все возможные ссылки
    for u in urls:

        _useragent = {'User-Agent': random.choice(list_of_user_agents)}
        _proxy = {'http': random.choice(list_of_viable_proxies)}
        _text = get_html_txt(u, _useragent, _proxy)
        time.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
        _soup = BeautifulSoup(_text, "html.parser")
        dir = os.path.abspath(os.curdir)
        write_to_file(dir, u, _soup)
        # if len(urls) > 200:
        #     break

        # находим ссылку
        for a in _soup.find_all('a'):
            if 'www' in a or ':' in a or 'http' in a:
                continue
            check = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+',a['href'])
            if len(check) > 0:
                continue
            link = main_url + a['href']
            if link not in urls:

                _useragent_ = {'User-Agent': random.choice(list_of_user_agents)}
                _proxy_ = {'http': random.choice(list_of_viable_proxies)}
                _text_ = get_html_txt(link, _useragent_, _proxy_)
                time.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
                _soup_ = BeautifulSoup(_text_, "html.parser")
                dir = os.path.abspath(os.curdir)
                write_to_file(dir, link, _soup_)
                urls.append(link)