from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

spiders = {
    'artsci_biology': True,
    'artsci_biology_goose': False,
    'artsci_biology_xpath': False,
    'artsci_chemistry': False,
    'artsci_exercise_science': False,
    'artsci_geography': False,
    'artsci_math': False,
    'artsci_physics': False,
    'artsci_psychology': False,
    'artsci_science_college': False,
}


project_settings = get_project_settings()
project_settings['CLOSESPIDER_ITEMCOUNT'] = 50
# project_settings['CLOSESPIDER_PAGECOUNT'] = 15
project_settings['DEPTH_LIMIT'] = 5
project_settings['CONCURRENT_REQUESTS'] = 10

configure_logging(project_settings)

runner = CrawlerRunner(project_settings)


@defer.inlineCallbacks
def crawl():
    for spider, v in spiders.iteritems():
        if v:
            yield runner.crawl(spider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished
