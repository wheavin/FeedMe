import feedparser

from parser.rss_channel import RssChannel


class RssUrlParser:

    def __init__(self, url):
        self.url = url

    def parse(self):
        rss_feed = feedparser.parse(self.url)
        self._validate_response(rss_feed)
        return self._create_rss_channel(rss_feed)

    def _validate_response(self, rss_feed):
        if not rss_feed:
            raise RssParserError("Invalid response returned for URL %s" % self.url)
        if 'bozo_exception' in rss_feed:
            raise RssParserError("Error parsing for URL %s" % self.url)

    def _create_rss_channel(self, rss_feed):
        feed = rss_feed['feed']
        title = feed['title']
        link = feed['link']
        description = feed['description']
        items = rss_feed['entries']
        return RssChannel(title, link, description, items)


class RssParserError(Exception):

    def __init__(self, message):
        self.message = message
