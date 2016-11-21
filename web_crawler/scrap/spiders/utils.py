import re
from urlparse import urlparse
from os.path import splitext, basename


def parse_body(response):
    """Parse html response text to retrieve the main content, using Xpath"""
    body = response.xpath("""//text()[normalize-space()
                                      and not(ancestor::div[contains (@class, 'c-back-to-top')])
                                      and not(ancestor::div[contains (@class, 'c-topnav top-links')])
                                      and not(ancestor::div[contains (@class, 'c-topnav top-links')])
                                      and not(ancestor::div[contains (@class, 'quick-links link-list')])
                                      and not(ancestor::div[contains (@class, 'parbase emergency-alert')])
                                      and not(ancestor::div[contains (@class, 'visible-print')])
                                      and not(ancestor::a |
                                              ancestor::script |
                                              ancestor::header |
                                              ancestor::noscript |
                                              ancestor::style |
                                              ancestor::footer)]""").extract()
    body = ' '.join(body)
    body = re.sub('\s+', ' ', body)
    return body


def allowed_links(base_url):
    """
    Given base url, retrieve the root path.
    It basically removes the extension in the url.
    Example: http://www.concordia.ca/artsci/biology.html ->
             /artsci/biology
    """
    disassembled = urlparse(base_url)
    _, ext = splitext(basename(disassembled.path))
    return disassembled.path.replace(ext, '')
