from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from scrap.spiders.utils import parse_body, allowed_links
from scrap.items import Article


class ArtsciBiologyXpathSpider(CrawlSpider):
    name = "artsci_biology_xpath"
    allowed_domains = ["concordia.ca"]
    start_urls = [
        'http://www.concordia.ca/artsci/biology.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=allowed_links(start_urls[0])), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.css('title::text').extract_first()

        body = parse_body(response)

        yield Article(title=title,
                      text=body,
                      url=response.url,
                      field=self.name)
