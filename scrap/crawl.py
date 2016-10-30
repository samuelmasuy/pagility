from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from scrap.spiders.artsci_biology import ArtsciBiologySpider
from scrap.spiders.artsci_biology_goose import ArtsciBiologyGooseSpider
# from scrap.spiders.artsci_chemistry import ArtsciChemistrySpider
# from scrap.spiders.artsci_exercise_science import ArtsciExerciseScienceSpider
# from scrap.spiders.artsci_geography import ArtsciGeographySpider
# from scrap.spiders.artsci_math import ArtsciGeographySpider
# from scrap.spiders.artsci_physics import ArtsciGeographySpider
# from scrap.spiders.artsci_psychology import ArtsciGeographySpider
# from scrap.spiders.artsci_science_college import ArtsciGeographySpider

spiders = {
    'artsci_biology': ArtsciBiologySpider,
    'artsci_biology_goose': ArtsciBiologyGooseSpider,
    #     'artsci_chemistry',
    #     'artsci_exercise_science',
    #     'artsci_geography',
    #     'artsci_math',
    #     'artsci_physics',
    #     'artsci_psychology',
    #     'artsci_science_college'
}


project_settings = get_project_settings()
project_settings['FEED_URI'] = 'output_%(name)s.json'
project_settings['FEED_FORMAT'] = 'jsonlines'
project_settings['CLOSESPIDER_ITEMCOUNT'] = 15
# project_settings['CLOSESPIDER_PAGECOUNT'] = 15
project_settings['DEPTH_LIMIT'] = 2
project_settings['LOG_LEVEL'] = 'INFO'
project_settings['CONCURRENT_REQUESTS'] = 16

configure_logging(project_settings)

runner = CrawlerRunner(project_settings)


@defer.inlineCallbacks
def crawl():
    for spider in spiders.iterkeys():
        yield runner.crawl(spider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished


# from scrapy.crawler import CrawlerProcess
# from scrapy.utils.project import get_project_settings


# spiders = [
#     'artsci_biology',
#     'artsci_chemistry',
#     'artsci_exercise_science',
#     'artsci_geography',
#     'artsci_math',
#     'artsci_physics',
#     'artsci_psychology',
#     'artsci_science_college'
# ]

# project_settings = get_project_settings()
# project_settings['FEED_FORMAT'] = 'json'
# project_settings['CLOSESPIDER_ITEMCOUNT'] = 15
# # project_settings['CLOSESPIDER_PAGECOUNT'] = 15
# project_settings['DEPTH_LIMIT'] = 2
# project_settings['LOG_LEVEL'] = 'INFO'
# project_settings['CONCURRENT_REQUESTS'] = 1


# def run_process(project_settings, spider):
#     project_settings['FEED_URI'] = '{}.json'.format(spider)

#     process = CrawlerProcess(project_settings)
#     process.crawl(spider)
#     process.start()


# if __name__ == '__main__':
#     # for spider in spiders:
#     #     run_process(project_settings, spider)
#     run_process(project_settings, 'artsci_biology')
#     run_process(project_settings, 'artsci_biology_goose')
