from atomicenergy.atomicenergyprovider import AtomicEnergyProvider
from rosenergoatom.rosenergoatomprovider import RosenergoatomProvider
from sdelanounas.sdelanounasprovider import SdelanoUNasProvider
from core.classification_job import ClassificationJob
import threading

class core_processor(object):

    list_of_jobs = [
        ClassificationJob()
    ]

    list_of_crawlers = [
        AtomicEnergyProvider(),
        RosenergoatomProvider(),
        SdelanoUNasProvider()
    ]

    def process(self):
        list_of_threads = []
        for crawler in self.list_of_crawlers:
            thread = threading.Thread(target=crawler.crawl)
            thread.setDaemon(True)
            thread.start()
            list_of_threads.append(thread)
        for job in self.list_of_jobs:
            thread = threading.Thread(target=job.process)
            thread.setDaemon(True)
            thread.start()
            list_of_threads.append(thread)
        for thread in list_of_threads:
            thread.join()

if __name__ == '__main__':
    core = core_processor()
    core.process()