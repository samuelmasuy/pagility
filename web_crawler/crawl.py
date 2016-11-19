import argparse

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


@defer.inlineCallbacks
def crawl():
    for spider, v in spiders.iteritems():
        if v:
            yield runner.crawl(spider)
    reactor.stop()


def get_cmd_args():
    """Helper function to get argument given to this program."""
    parser = argparse.ArgumentParser(description="Crawl different artsci departments from Concordia Uninversity.")

    parser.add_argument(
        "--item-count",
        dest="item_count",
        type=int,
        default=50,
        help="Limit the number of items (website) to crawl."
    )
    parser.add_argument(
        "--depth-limit",
        dest="depth_limit",
        type=int,
        default=5,
        help="Limit the maximum depth to which the crawling will go."
    )
    parser.add_argument(
        "--concurrent-requests",
        dest="concurrent_requests",
        type=int,
        default=10,
        help="Limit the number of concurrent requests the crawler can do."
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = get_cmd_args()

    project_settings = get_project_settings()
    project_settings['CLOSESPIDER_ITEMCOUNT'] = args.item_count
    # project_settings['CLOSESPIDER_PAGECOUNT'] = 15
    project_settings['DEPTH_LIMIT'] = args.depth_limit
    project_settings['CONCURRENT_REQUESTS'] = args.concurrent_requests

    configure_logging(project_settings)

    runner = CrawlerRunner(project_settings)

    crawl()
    reactor.run() # the script will block here until the last crawl call is finished
