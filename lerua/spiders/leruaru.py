import scrapy
from scrapy.http import HtmlResponse
from lerua.items import LeruaItem
from scrapy.loader import ItemLoader


class LeruaruSpider(scrapy.Spider):
    name = 'leruaru'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://leroymerlin.ru']

    def __init__(self, search):
        super(LeruaruSpider, self).__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        goods_links = response.xpath("//a[@class='plp-item__info__title']/@href").extract()

        for good in goods_links:
            yield response.follow(good, callback=self.parse_goods)

        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_goods(self, response: HtmlResponse):
        loader = ItemLoader(item=LeruaItem(), response=response)
        loader.add_xpath('_id', "//span[@slot='article']/@content")  # запишем в ИД артикул товара
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@slot='thumbs']/@src")

        # Соберем словарь с Характеристиками товара
        def_dict = {}
        def_list = response.xpath("//div[@class='def-list__group']")  # блок с характеристиками
        for def_row in def_list:
            a = def_row.xpath(".//dt/text()").extract_first()
            b = (def_row.xpath(".//dd/text()").extract_first()).split('\n')
            b = b[1].lstrip()
            def_dict[a] = b
        loader.add_value('def_list', def_dict)

        yield loader.load_item()
