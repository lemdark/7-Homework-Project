import scrapy


class QSpider(scrapy.Spider):
    name = 'qspider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/']

    current = 0
    max_page = 1

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response):
        rows = response.xpath("//div[contains(@class, 'quote')]")
        for row in rows:
            text = row.xpath("./span[contains(@class, 'text')]/text()").get()
            author = row.xpath("./span/small[contains(@class, 'author')]/text()").get()
            yield {
                "text": text,
                "author": author,
            }

        # Follow the next page link
        next_page = response.xpath("//li[@class='next']/a/@href").get()
        if next_page is not None and self.current < self.max_page:
            self.current += 1
            yield response.follow(next_page, callback=self.parse)
