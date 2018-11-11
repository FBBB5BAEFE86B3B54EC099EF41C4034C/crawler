import random
import time

import requests
from bs4 import BeautifulSoup
from dateutil.parser import *
from proxy.proxy_getter import get_html_proxy
from proxy.proxy_getter import get_viable_proxy_list
from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory
import traceback


list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'), 10)
list_of_user_agents = open('../proxy/useragents.txt').read().split('\n')
# Подсчет кол-ва статей
numberArticle = 0
elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()


def get_html(url, user_agent, proxy):
    # при выполнении get получаем ответ Response 200. Это означает что все ок.
    r = requests.get(url, timeout=None, proxies={'': proxy})
    return r.text


def NewArticleUrl(start_url):
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    # header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '29278?PAGEN_1=')
    count = 7
    global numberArticle

    while (count >= 0):
        page_url = "%s%s" % (web_url, count)
        code = get_html(page_url, useragent, proxy)
        # plain = code.text
        s = BeautifulSoup(code, "html.parser")
        count -= 1

        for a in s.findAll('p', {'class': 'news-item'}):
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = item_id[item_start:length:1] + '/'
            Crawler("%s%s" % (start_url, item))
            numberArticle += 1


def OldArticleUrl(start_url):
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    # header = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    web_url = "%s%s" % (start_url, '?PAGEN_1=')
    count = 0
    global numberArticle

    # Определение кол-ва страниц
    url_pages = "%s%s" % (web_url, 0)
    code_pages = get_html(url_pages, useragent, proxy)
    # code_pages = requests.get(url_pages, headers=header)
    soup_page = BeautifulSoup(code_pages, "html.parser")
    pages = soup_page.find('a', {'class': 'modern-page-dots'}).find_next_sibling('a')

    while (count <= int(pages.text)):
        page_url = "%s%s" % (web_url, count)
        # code = requests.get(page_url)
        # code = requestGet(page_url)
        code = get_html(page_url, useragent, proxy)
        # plain = code.text
        s = BeautifulSoup(code, "html.parser")
        count += 1
        head = s.findAll('div', {'class': 'news-list'})[2]

        for a in head.findAll('p', {'class': 'news-item'}):
            item_id = a.get('id')
            length = len(item_id)
            item_start = item_id.rfind('_', 0, length) + 1
            item = 'index.php?ELEMENT_ID=' + item_id[item_start:length:1]
            Crawler("%s%s" % (start_url, item))
            numberArticle += 1


def Crawler(url):
    global content, date, tag, title
    time.sleep(round(abs(random.gauss(1.5, 1) + random.random() / 10 + random.random() / 100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}

    code = get_html(url, useragent, proxy)
    soup = BeautifulSoup(code, "html.parser")

    # Дата
    try:
        div = soup.find('div', {'id': 'content'})
        date = div.find('span', {'class': 'news-date-time'})
        date = parse(date.text).date()
    except:
        pass
    # Tag
    # tag = soup.find('div', {'class':'col-lg-6 content-block'}).find('h1')
    try:
        tag = div.find('small', {'class': 'sourcetext'})
    except:
        pass
    # Заголовок
    try:
        title = div.find('p', {'class': 'detnewsTitle'})
    except:
       pass

    # Статья
    try:
        content = div.find('div').find('div')
    except:
        pass

    try:
        if not(elasticsearchCrawlerClient.contains(url)):
            elasticsearchCrawlerClient.put(url,
                                           content.text.strip().replace("\n", ""),
                                           date,
                                           title.text.strip(),
                                           tag.text.strip())
    except Exception:
        print('Ошибка записи в базу')
        traceback.print_exc()



def crawl():
    # Статьи за 2017-2018
    NewArticleUrl('http://www.rosenergoatom.ru/zhurnalistam/novosti-otrasli/')

    # Статьи за 2010-2016
    year = 2010
    while (year <= 2016):
        old_url = 'http://www.rosenergoatom.ru/zhurnalistam/news-archive/'
        year_url = str(year) + '/'
        OldArticleUrl("%s%s" % (old_url, year_url))
        year += 1
