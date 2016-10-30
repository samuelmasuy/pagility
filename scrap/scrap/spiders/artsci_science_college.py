from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrap.spiders.body_parser import parse_body


class QuotesSpider(CrawlSpider):
    name = "artsci_science_college"
    start_urls = [
        'http://www.concordia.ca/artsci/science-college.html',
    ]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.css('title::text').extract_first()

        body = parse_body(response)

        yield {
                'url': response.url,
                'title': title,
                'body': body,
        }
