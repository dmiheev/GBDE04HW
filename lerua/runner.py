from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lerua.spiders.leruaru import LeruaruSpider
from lerua import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeruaruSpider, search='снегоуборочные машины')
    process.start()
