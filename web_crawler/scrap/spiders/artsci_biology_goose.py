from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from goose import Goose

from scrap.items import Article
from scrap.spiders.utils import allowed_links


class ArtsciBiologyGooseSpider(CrawlSpider):
    name = "artsci_biology_goose"
    allowed_domains = ["concordia.ca"]
    start_urls = [
        'http://www.concordia.ca/artsci/biology.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=allowed_links(start_urls[0])), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        article = Goose().extract(raw_html=response.body)

        yield Article(title=article.title,
                      text=article.cleaned_text,
                      url=response.url,
                      field=self.name)
