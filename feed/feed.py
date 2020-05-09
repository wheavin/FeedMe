#!/usr/bin/python3
"""
Responsible for handling the RSS feed data.
"""

from parser.rss_parser import RssUrlParser, RssParserError


def fetch_content_for_feed_url(rss_feed_url):
    """
    Returns the feed content for a provided RSS feed url.
    :param rss_feed_url:
    :return:
    """
    feed_content = "No RSS feed content to display"
    rss_url_parser = RssUrlParser(rss_feed_url)
    try:
        feed_content = rss_url_parser.parse()
    except RssParserError as error:
        print(error.message)
    return feed_content


class RssFeedError(Exception):
    """
    Thrown when an error occurs when updating RSS feed.
    """

    def __init__(self, message):
        super(RssFeedError, self).__init__(message)
        self.message = message
