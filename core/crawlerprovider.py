import time


class CrawlerProvider:

    def process_crawler(self, retry=False, delay_between_execute_seconds=100000):

        while True:
            try:
                self.crawl()
            except Exception:
                print("Error while parsing")
            if not retry:
                break
            else:
                time.sleep(delay_between_execute_seconds)

    def crawl(self):
        raise Exception("Not implemented method")
