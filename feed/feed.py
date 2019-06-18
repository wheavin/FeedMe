import os

from parser.rss_parser import RssUrlParser

RSS_FEED_URLS_FILENAME = os.path.join(os.path.dirname(__file__), 'data/rss_feeds.txt')
RSS_FEED_CONTENT_FILENAME = os.path.join(os.path.dirname(__file__), 'data/rss_feed_content.txt')


class Feed:

    def __init__(self):
        self.rss_feed_urls = self._get_rss_feed_urls()

    def _get_rss_feed_urls(self):
        rss_feed_urls = []
        with open(RSS_FEED_URLS_FILENAME) as rss_url_file:
            for url in rss_url_file:
                rss_feed_urls.append(url)
        return rss_feed_urls

    def refresh_content(self):
        for rss_feed_url in self.rss_feed_urls:
            rss_url_parser = RssUrlParser(rss_feed_url)
            feed_content = rss_url_parser.parse()
            self._write_feed_contents(feed_content)

    def _write_feed_contents(self, feed_content):
        with open(RSS_FEED_CONTENT_FILENAME, "w") as feed_content_file:
            feed_content_file.write(feed_content)
        feed_content_file.close()
