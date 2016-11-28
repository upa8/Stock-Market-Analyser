import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/'
    ]

    def parse(self, response):
        print "Printing data"
        print response.body

QuotesSpider = QuotesSpider();
QuotesSpider.parse();
