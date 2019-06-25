"""
Parser for RSS feeds.
"""

from parser.rss_channel import RssChannel

import feedparser


def _validate_rss_channel(rss_feed):
    if "feed" not in rss_feed or "entries" not in rss_feed:
        raise RssParserError("Invalid RSS channel data: %s" % rss_feed)
    feed = rss_feed['feed']
    if "title" not in feed or "link" not in feed or "description" not in feed:
        raise RssParserError("Invalid RSS channel data: %s" % rss_feed)


def _create_rss_channel(rss_feed):
    _validate_rss_channel(rss_feed)
    feed = rss_feed['feed']
    title = feed['title']
    link = feed['link']
    description = feed['description']
    items = rss_feed['entries']
    return RssChannel(title, link, description, items)


class RssUrlParser:
    """
    Parses RSS feed data from given RSS feed URL.
    """

    def __init__(self, url):
        self.url = url

    def parse(self):
        """
        Parses RSS feed data from given RSS feed URL.
        :return: the formatted RSS feed data.
        """
        rss_feed = feedparser.parse(self.url)
        self._validate_response(rss_feed)
        rss_channel = _create_rss_channel(rss_feed)
        return rss_channel.format_feed_content()

    def _validate_response(self, rss_feed):
        if not rss_feed:
            raise RssParserError("Invalid response returned for URL %s" % self.url)
        if 'bozo_exception' in rss_feed:
            raise RssParserError("Error parsing for URL %s" % self.url)


class RssParserError(Exception):
    """
    Exception is thrown when RSS feed response is invalid.
    """

    def __init__(self, message):
        super(RssParserError, self).__init__(message)
        self.message = message
