#!/usr/bin/python3
"""
Responsible for handling the RSS feed data.
"""

from parser.rss_parser import RssUrlParser


class Feed:
    """
    RSS feed data.
    """

    def __init__(self, rss_feed_urls):
        self.rss_feed_urls = rss_feed_urls

    def refresh_content(self):
        """
        Gets the feed content for each RSS feed url and writes this content to the data file.
        :return:
        """
        if not self.rss_feed_urls:
            raise RssFeedError("No RSS feed URLs found")

        feed_content = ""
        for rss_feed_url in self.rss_feed_urls.get_urls():
            rss_url_parser = RssUrlParser(rss_feed_url)
            feed_content += rss_url_parser.parse()
        return feed_content


class RssFeedError(Exception):
    """
    Thrown when an error occurs when updating RSS feed.
    """

    def __init__(self, message):
        super(RssFeedError, self).__init__(message)
        self.message = message


if __name__ == '__main__':
    feed = Feed()
    feed.refresh_content()
