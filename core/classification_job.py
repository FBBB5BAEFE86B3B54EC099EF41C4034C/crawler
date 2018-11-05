from repository.DocumentStateManager import DocumentStateManager
from repository.ElasticsearchCrawlerClient import ElasticsearchCrawlerClientFactory
from classification.TextREAClassificator import Classifier
import traceback
import time

class ClassificationJob(object):

    def __init__(self, delayBeforeProcess = 60):
        self.delay = delayBeforeProcess
        self.elasticsearchCrawlerClient = ElasticsearchCrawlerClientFactory().getSingleton()
        self.classifier = Classifier()

    def process(self):
        while True:
            try:
             documentManager = DocumentStateManager(self.elasticsearchCrawlerClient)
             if documentManager.document != None:
                clаss = self.classifier.text(documentManager.document['data'])[0]
                if clаss != '':
                    documentManager.change_state(clаss)
            except:
                print("EXCEPTION WHILE CHANGE CLASS")
                traceback.print_exc()
                pass
            time.sleep(self.delay)




