from rosenergoatom import crawler as crawler
from core.crawlerprovider import CrawlerProvider

class RosenergoatomProvider(CrawlerProvider):

    def crawl(self):
        crawler.crawl()



