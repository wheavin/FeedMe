#!/usr/bin/python3
"""
Parser for RSS feeds.
"""

from parser.rss_channel import RssChannel

import feedparser


def _validate_rss_channel(rss_feed):
    if "feed" not in rss_feed or "entries" not in rss_feed:
        raise RssParserError("Invalid RSS channel data: %s" % rss_feed)
    feed = rss_feed['feed']
    if "title" not in feed or "link" not in feed:
        raise RssParserError("Invalid RSS channel data: %s" % rss_feed)


def _create_rss_channel(rss_feed):
    _validate_rss_channel(rss_feed)
    feed = rss_feed['feed']
    title = feed['title']
    link = feed['link']

    try:
        description = feed['description']
    except KeyError:
        description = feed['subtitle']

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
        if not self.url:
            raise RssParserError("Error parsing for URL %s" % self.url)

        print("Parsing RSS feed for URL:", self.url)
        rss_feed_response = feedparser.parse(self.url)
        self._validate_response(rss_feed_response)
        rss_channel = _create_rss_channel(rss_feed_response)
        return rss_channel.format_feed_content()

    def _validate_response(self, rss_feed_response):
        if not rss_feed_response:
            raise RssParserError("Invalid response returned for URL %s" % self.url)
        if 'bozo_exception' in rss_feed_response:
            raise RssParserError("Error parsing for URL %s" % self.url)
        print("Successfully validated response.")


class RssParserError(Exception):
    """
    Exception is thrown when RSS feed response is invalid.
    """

    def __init__(self, message):
        super(RssParserError, self).__init__(message)
        self.message = message
