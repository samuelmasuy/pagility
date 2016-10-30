from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from goose import Goose
# from scrap.spiders.body_parser import parse_body
from scrap.items import Article


class QuotesSpider(CrawlSpider):
    name = "artsci_biology_goose"
    allowed_domains = ["concordia.ca"]
    start_urls = [
        'http://www.concordia.ca/artsci/biology.html',
    ]

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        # page = response.url.split("/")[-1]
        # filename = 'artsci-%s.html' % page
        # title = response.css('title::text').extract_first()

        # body = parse_body(response)
        # description = response.xpath("//meta[@name='description']").extract_first()
        # description = response.xpath("//meta/@content").extract()
        article = Goose().extract(raw_html=response.body)

        yield Article(title=article.title,
                      text=article.cleaned_text,
                      url=response.url,
                      field=self.name)
        # yield {
        #         'url': response.url,
        #         'title': title,
        #         'body': body,
        # }
        # self.log('Saved file %s' % filename)
