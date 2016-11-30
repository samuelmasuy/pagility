from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from boilerpipe.extract import Extractor

from scrap.items import Article
from scrap.spiders.utils import allowed_links


class ArtsciMysterySpider(CrawlSpider):
    name = "artsci_mystery"
    allowed_domains = ["concordia.ca"]
    start_urls = [
        'https://www.concordia.ca/artsci/science-college/about/life-at-the-college.html',
    ]

    rules = (
        Rule(LinkExtractor(allow=allowed_links(start_urls[0])), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.css('title::text').extract_first()

        extractor = Extractor(extractor='ArticleExtractor', html=response.body)

        yield Article(title=title,
                      text=extractor.getText(),
                      url=response.url,
                      field=self.name)
