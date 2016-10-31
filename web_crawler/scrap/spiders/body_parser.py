import re


def parse_body(response):
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
