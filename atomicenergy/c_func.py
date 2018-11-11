import requests
from dateutil.parser import *


from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory
elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()


def get_html_txt(url, useragent, proxy):

    r = requests.get(url, headers=useragent, timeout = None, proxies = {'': proxy})
    return r.text

def write_to_file(dir, link, _soup_):


        # Ссылка
        # Опрелеляем заголовок
        title = ''
        try:
            title = _soup_.find('div', {'class':'clearfix'}).find('h1').text
        except:
            pass
        # Находим данные, если есть
        ps = _soup_.find_all('p')
        data = ''
        try:
            for p in ps:
                data += p.text + '\n'
        except:
            pass
        # находим дату, если есть
        date = ''
        try:
            date = ''.join([c if c not in ['\n','\t'] else '' for c in _soup_.find('div', {'class': 'node-meta__date'}).text])
        except Exception as e:
            date = 'no date '
        # определяем тэги
        try:
            tags = _soup_.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
            content = tags.find('div', {'class': 'content'}).find_all('div', class_="title")
            t = []
            for tag in content:
                te = tag.find('a').text
                sp = tag.find('span').text
                t.append(te + sp + ' ')
        except Exception as e:
            pass

        try:
            key_ = link
            data_ = data
            date_ = parse(date).date()
            tags_ = t
            head_ = title
            if elasticsearchCrawlerClient.contains(key_):
                pass
            else:
                if data.strip() != '' and (date_ != None and date != ''):
                    elasticsearchCrawlerClient.put(key_, data_, date_, tags_, head_)
        except:
            pass