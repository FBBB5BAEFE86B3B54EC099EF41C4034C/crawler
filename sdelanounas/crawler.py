import requests
from bs4 import BeautifulSoup

def crawl(webUrl):
    url = webUrl
    code = requests.get(url)
    plain = code.text
    s = BeautifulSoup(plain, "html.parser")
    f = open("crawlerResult.txt", mode='a', encoding='utf8')

    #Дата статьи
    date = s.findAll('li', {'class':'time'})[0]
    if len(date.findAll('span')):
        date.span.replace_with(" ")
    dateText = "%s %s\n" % ("DATE:", date.text)

    #Данные за 2016-2018 года
    if ("2018" in dateText) or ("2017" in dateText) or ("2016" in dateText):
        #URL
        urlText = "%s %s\n" % ("URL:", webUrl)
        print(urlText)
        f.write(urlText)

        #Заголовок статьи
        header = ""
        if len(s.findAll('h1', {'class':'h1_openblog'})):
            header = s.findAll('h1', {'class':'h1_openblog'})[0]
        else:
            header = s.findAll('h1', {'class':'unique'})[0]
        headerText = "%s %s\n" % ("HEADER:", header.text.strip())
        print(headerText)
        f.write(headerText)

        #Содержимое статьи
        content = []
        article = s.findAll('div', {'class':'text __sun_article_text'})[0]
        while len(article.findAll('ul')):
            article.ul.replace_with("")
        while len(article.findAll('li')):
            article.ul.replace_with("")
        while len(article.findAll('span')):
            article.span.replace_with("")
        while len(article.findAll('div')):
            article.div.replace_with("")
        content.append("" if article.text is None else article.text.replace("\n", ""))
        if article.string is None:
            for p in s.findAll('p'):
                if not(p.text is None) and (p.find_parent("div") is None):
                    content.append(p.text)
        else:
            for p in article.findAll('p'):
                if not(p.text is None):
                    content.append(p.text)
        contentText = "%s %s\n" % ("CONTENT:", "".join(content))
        print(contentText)
        f.write(contentText)

        #Дата статьи
        print(dateText)
        f.write(dateText)

        #Теги
        tags = []
        for tag in s.findAll('a', {'class':'article-tag'}):
            tags.append(tag.text)
        tagsText = "%s %s\n" % ("TAGS:", ", ".join(tags))
        print(tagsText)
        f.write(tagsText)

        #Разделитель
        separatorText = "__________________________________________________________________________________\n"
        print(separatorText)
        f.write(separatorText)

    f.close()


def collectUrls(baseUrl, searchUrl):
    f = open("crawlerResult.txt", "w")
    f.close()
    flag = True
    count = 0

    #Обходим все ссылки в поиске по сайту по "Росэнергоатом"
    while(flag):
        flag = False
        url = "%s%s" % (searchUrl, count)
        code = requests.get(url)
        plain = code.text
        s = BeautifulSoup(plain, "html.parser")
        count += 1

        for heading in s.findAll('div', {'class':'heading'}):
            crawl("%s%s" % (baseUrl, heading.h4.a.get('href')))
            #crawl("%s%s" % ('http://www.sdelanounas.ru', '/blogs/107618'))
            flag = True