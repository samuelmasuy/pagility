from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


spiders = [
    'artsci_biology',
    'artsci_chemistry',
    'artsci_exercise_science',
    'artsci_geography',
    'artsci_math',
    'artsci_physics',
    'artsci_psychology',
    'artsci_science_college'
]

project_settings = get_project_settings()
project_settings['FEED_FORMAT'] = 'json'
project_settings['CLOSESPIDER_ITEMCOUNT'] = 15
# project_settings['CLOSESPIDER_PAGECOUNT'] = 15
project_settings['DEPTH_LIMIT'] = 2
project_settings['LOG_LEVEL'] = 'INFO'
project_settings['CONCURRENT_REQUESTS'] = 1


def run_process(project_settings, spider):
    project_settings['FEED_URI'] = '{}.json'.format(spider)

    process = CrawlerProcess(project_settings)
    process.crawl(spider)
    process.start()


if __name__ == '__main__':
    # for spider in spiders:
    #     run_process(project_settings, spider)
    run_process(project_settings, 'artsci_biology')
    run_process(project_settings, 'artsci_biology_goose')
