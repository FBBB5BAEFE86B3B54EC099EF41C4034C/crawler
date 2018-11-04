from sdelanounas import crawler as crawler
from core.crawlerprovider import CrawlerProvider

class SdelanoUNasProvider(CrawlerProvider):

    baseUrl = 'http://www.sdelanounas.ru'
    startPage = 'http://www.sdelanounas.ru/sphinxsearch/?s=росэнергоатом&page='

    def crawl(self):
        crawler.CollectUrls(baseUrl=self.baseUrl, searchUrl=self.startPage)






