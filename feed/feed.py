#!/usr/bin/python3
"""
Responsible for handling the RSS feed data.
"""

from parser.rss_parser import RssUrlParser, RssParserError


class Feed:
    """
    RSS feed data.
    """

    def __init__(self, rss_feed_urls=None):
        self.rss_feed_urls = rss_feed_urls

    def refresh_content(self):
        """
        Gets the feed content for each RSS feed url and writes this content to the data file.
        :return:
        """
        feed_content = []
        if self.rss_feed_urls:
            for rss_feed_url in self.rss_feed_urls:
                rss_url_parser = RssUrlParser(rss_feed_url)
                try:
                    feed_content.append(rss_url_parser.parse())
                except RssParserError as error:
                    print(error.message)

        return feed_content if feed_content else ["No RSS feed content to display"]

    def fetch_content_for_feed_url(self, rss_feed_url):
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
