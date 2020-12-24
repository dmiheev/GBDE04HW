import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    # пособираем Стивена Кинга
    start_urls = ['https://www.labirint.ru/search/%D1%81%D1%82%D0%B8%D0%B2%D0%B5%D0%BD%20%D0%BA%D0%B8%D0%BD%D0%B3/?stype=0']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[@class='product-title-link']/@href").extract()

        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//div[@class='authors']/a/text()").extract_first()
        price = response.xpath("//span[@class='buying-pricenew-val-number' "
                               "or @class='buying-price-val-number']/text()").extract_first()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        rating = response.xpath("//div[@id='rate']/text()").extract_first()
        yield BookparserItem(link=link, name=name, author=author, price=price, old_price=old_price, rating=rating)
