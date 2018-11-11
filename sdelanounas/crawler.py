import random
import time as tm
import requests
from bs4 import BeautifulSoup
from dateutil.parser import *

from proxy.proxy_getter import get_html_proxy
from proxy.proxy_getter import get_viable_proxy_list
from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory


def Crawl(webUrl):
    url = webUrl
    html = getHtmlWithProxy(url)
    s = BeautifulSoup(html, "html.parser")
    hasError = False

    #Дата статьи
    try:
        date = s.findAll('li', {'class':'time'})[0]
        if date.findAll('span'):
            date.span.replace_with(" ")
        date = date.text
        date = parse(date).date()
    except Exception as e:
        print("Исключение при определении даты статьи", url, e)
        date = ""
        hasError = True

    #Заголовок статьи
    header = ""
    try:
        if s.findAll('h1', {'class':'h1_openblog'}):
            header = s.findAll('h1', {'class':'h1_openblog'})[0]
        else:
            header = s.findAll('h1', {'class':'unique'})[0]
        header = header.text.strip()
    except Exception as e:
        print("Исключение при определении заголовка статьи", url, e)
        header = ""

    #Содержимое статьи
    try:
        content = []
        article = s.findAll('div', {'class':'text __sun_article_text'})[0]
        if (article.text == '\n'):
            article = s.contents[4]
        else:
            while article.findAll('li'):
                article.li.replace_with("")
        while article.findAll('div'):
            article.div.replace_with("")
        content.append("" if article.text is None else article.text.replace("\n", ""))
        content = "".join(content)
    except Exception as e:
        print("Исключение при определении содержимого статьи", url, e)
        content = ""
        hasError = True

    #Теги
    tags = []
    try:
        for tag in s.findAll('a', {'class':'article-tag'}):
            tags.append(tag.text)
    except Exception as e:
        print("Исключение при определении тегов статьи", url, e)
        tags = []
        hasError = True
    tags = ", ".join(tags)

    # Обращение к внешнему объекту elasticsearchCrawlerClient
    try:
        if not(elasticsearchCrawlerClient.contains(url)) and not(hasError):
            elasticsearchCrawlerClient.put(url, content, date, header, tags)
    except Exception as e:
        print('Исключение при записи в БД', e)


def CollectUrls(baseUrl, searchUrl):
    flag = True
    count = 0

    #Обходим все ссылки в поиске по сайту по "Росэнергоатом"
    while(flag):
        try:
            flag = False
            url = "%s%s" % (searchUrl, count)
            html = getHtmlWithProxy(url)
            s = BeautifulSoup(html, "html.parser")
            count += 1

            for heading in s.findAll('div', {'class':'heading'}):
                flag = True
                Crawl("%s%s" % (baseUrl, heading.h4.a.get('href')))
                #Crawl("%s%s" % ('http://www.sdelanounas.ru', '/blogs/5307'))
        except Exception as e:
            print('Исключение в CollectUrls', e)
            continue

def getHtmlWithProxy(url):
    tm.sleep(round(abs(random.gauss(1.5, 1) + random.random()/10 + random.random()/100), 4))
    useragent = {'User-Agent': random.choice(list_of_user_agents)}
    proxy = {'http': random.choice(list_of_viable_proxies)}
    r = requests.get(url, timeout = None, headers = useragent, proxies = {'': proxy})
    return r.text


elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()
#Proxy
list_of_viable_proxies = get_viable_proxy_list(get_html_proxy('https://www.ip-adress.com/proxy-list'),10)
list_of_user_agents = open('proxy/useragents.txt').read().split('\n')