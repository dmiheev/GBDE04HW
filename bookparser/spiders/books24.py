import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Books24Spider(scrapy.Spider):
    name = 'books24ru'
    allowed_domains = ['book24.ru']
    # пособираем Стивена Кинга
    start_urls = ['https://book24.ru/search/?q=%D1%81%D1%82%D0%B8%D0%B2%D0%B5%D0%BD%20%D0%BA%D0%B8%D0%BD%D0%B3']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath("//a[@class='book-preview__image-link']/@href").extract()

        for book in book_links:
            yield response.follow(book, callback=self.book_parse)

        next_page = response.xpath("//a[text()='Далее']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        link = response.url
        name = response.xpath("//h1/text()").extract_first()
        author = response.xpath("//a[@itemprop='author']/text()").extract_first()
        price = response.xpath("//div[@class='item-actions__price']/b/text()").extract_first()
        old_price = response.xpath("//div[@class='item-actions__price-old']/text()").extract_first()
        rating = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        yield BookparserItem(link=link, name=name, author=author, price=price, old_price=old_price, rating=rating)
