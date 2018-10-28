from atomicenergy import crawler as crawler
from core.crawlerprovider import CrawlerProvider

class AtomicEnergyProvider(CrawlerProvider):

    def crawl(self):
        crawler.crawler()
