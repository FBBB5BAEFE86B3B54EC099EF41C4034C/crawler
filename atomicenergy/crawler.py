import os

import requests
# from lxml import html
from bs4 import BeautifulSoup
from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory

elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()

def crawler():
    header = {'User-Agent':
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'}
    url_majors = 'http://www.atomic-energy.ru'
    links = ('why-nuclear', '2.0')

    req = requests.get(url_majors, headers = header)
    soup = BeautifulSoup(req.text, "html.parser")
    li = soup.find('nav').find('ul').find_all('li')

    mass = []
    for l in li:
        l.find('a', href = True)
        href = l.find('a', href = True)['href']
        if 'http' in href or href == '/':
            continue
        loc_req = requests.get(url_majors+href, headers = header)

        soup = BeautifulSoup(loc_req.text, "html.parser")
        dir = os.path.abspath(os.curdir)
        with open(dir+'/'+'file'+'.txt','a') as f:
            title = soup.find('div', {'class':'clearfix'}).find('h1').text
            f.write('URL: ' + url_majors+href + '\n')
            f.write('HEADER: ' + ''.join([c if c not in ['\n','\t'] else '' for c in title]) + '\n')
            ps = soup.find_all('p')
            f.write('CONTENT: ')
            for p in ps:
                f.write(p.text + ' ')
            f.write('\n')
            try:
                f.write('DATE: ' + ''.join([c if c not in ['\n','\t'] else '' for c in soup.find('div', {'class': 'node-meta__date'}).text]) + '\n')
            except Exception as e:
                f.write('DATE: ' + 'no date ' + '\n')
            f.write('\n')
            try:
                tags = soup.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
                content = tags.find('div', {'class': 'content'}).find_all('div', class_="title")
                f.write('TAGS: ')
                for tag in content:
                    te = tag.find('a').text
                    sp = tag.find('span').text
                    f.write(te + sp + ' ')
                f.write('\n')
            except Exception as e:
                f.write('TAGS: ' + '\n')

            f.write(''.join(['-' for i in range(50)]) + '\n')

        for x in soup.find_all('a'):
            if ':' in x['href']:
                continue
            elif x['href'] in mass:
                continue


            mass.append(x['href'])
            urlText = url_majors+x['href']
            headerText = ''.join([c if c not in ['\n','\t'] else '' for c in title])
            contentText = ''
            dateText = ''
            tagsText = []

            try:
                with open(dir+'/'+'file'+'.txt','a') as f:
                    ll_rec = requests.get(url_majors+x['href'], headers = header)
                    loc_soup = BeautifulSoup(ll_rec.text, "html.parser")
                    l_title = loc_soup.find('div', {'class':'clearfix'}).find('h1').text

                    f.write('URL: ' + url_majors+x['href'] + '\n')
                    f.write('HEADER: ' + ''.join([c if c not in ['\n','\t'] else '' for c in title]) + '\n')
                    f.write('CONTENT: ')
                    for te in loc_soup.find_all('p'):
                        f.write(te.text + ' ')
                    f.write('\n')
                    content = ''
                    for te in loc_soup.find_all('p'):
                        content += te.text + '\n'

                    contentText = content

                    try:
                        dateText = ''.join([c if c not in ['\n','\t'] else '' for c in loc_soup.find('div', {'class': 'node-meta__date'}).text])
                        f.write('DATE: ' + ''.join([c if c not in ['\n','\t'] else '' for c in loc_soup.find('div', {'class': 'node-meta__date'}).text]) + '\n')
                    except:
                        f.write('DATE: ' + 'no Date ' + '\n')
                    # Теги
                    f.write('\n')
                    try:
                        tags = loc_soup.find('div', {'class': 'block-atom-sidebar-taxonomy block block-atom-sidebar clearfix'})
                        content = tags.find('div', {'class': 'content'}).find_all('div', class_="title")
                        f.write('TAGS: ')
                        for tag in content:
                            te = tag.find('a').text
                            sp = tag.find('span').text
                            f.write(te + sp + ' ')
                            tagsText.append(te + sp)
                        f.write('\n')
                    except:
                        f.write('TAGS: ' + '\n')
                    f.write(''.join(['-' for i in range(50)]) + '\n')
            except Exception as e:
                pass

            try:
                if elasticsearchCrawlerClient.contains(urlText):
                    pass
                else:
                    if contentText != '':
                        elasticsearchCrawlerClient.put(urlText, contentText, dateText, headerText, tagsText)
            except:
                pass