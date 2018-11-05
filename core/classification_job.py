from repository.DocumentStateManager import DocumentStateManager
from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory
import time

class ClassificationJob(object):

    def __init__(self, delayBeforeProcess = 60):
        self.delay = delayBeforeProcess
        self.elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()

    def process(self):
        while True:
            try:
             documentManager = DocumentStateManager(self.elasticsearchCrawlerClient)
             # todo: Implement classification call
            except:
                pass
            time.sleep(self.delay)




