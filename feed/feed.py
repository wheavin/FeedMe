"""
Responsible for handling the RSS feed data.
"""

from parser.rss_parser import RssUrlParser
from utils.files import get_full_path

RSS_FEED_URLS_FILENAME = get_full_path("data", "rss_feeds.txt")
RSS_FEED_CONTENT_FILENAME = get_full_path("data", "rss_feed_content.txt")


def _write_feed_contents(feed_content):
    with open(RSS_FEED_CONTENT_FILENAME, "w") as feed_content_file:
        feed_content_file.write(feed_content)
    feed_content_file.close()


def _get_rss_feed_urls():
    rss_feed_urls = []
    try:
        with open(RSS_FEED_URLS_FILENAME) as rss_url_file:
            for url in rss_url_file:
                rss_feed_urls.append(url)
    except FileNotFoundError:
        raise RssFeedError("No RSS feed file found for %s" % RSS_FEED_URLS_FILENAME)
    return rss_feed_urls


class Feed:
    """
    RSS feed data.
    """

    def __init__(self):
        self.rss_feed_urls = _get_rss_feed_urls()

    def refresh_content(self):
        """
        Gets the feed content for each RSS feed url and writes this content to the data file.
        :return:
        """
        if not self.rss_feed_urls:
            raise RssFeedError("No RSS feed URLs found")

        feed_content = ""
        for rss_feed_url in self.rss_feed_urls:
            rss_url_parser = RssUrlParser(rss_feed_url)
            feed_content += rss_url_parser.parse()
        _write_feed_contents(feed_content)


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
