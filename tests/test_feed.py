import os
from unittest.mock import patch

from pyfakefs import fake_filesystem_unittest

from feed.feed import Feed
from tests.test_utils.file_reader import TextFileReader

DATA_FILE_PATH = "/home/william/Development/git/FeedMe/feed/data/"
RSS_FEED_CONTENT_FILENAME = DATA_FILE_PATH + "rss_feed_content.txt"
RSS_FEED_URLS_FILENAME = DATA_FILE_PATH + "rss_feeds.txt"


class TestFeed(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        self.file_reader = TextFileReader(RSS_FEED_CONTENT_FILENAME)

    @patch("feedparser.parse")
    def test_refresh(self, mock_response):
        # Given: a feed instance
        self._prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
        obj_under_test = Feed()
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"}, "entries": []
        }
        # When: the feed is refreshed
        obj_under_test.refresh_content()

        # Then: the feed contents have been updated
        current_content = self.file_reader.read()
        self.assertIn("FierceWireless", current_content)
        self.assertIn("some link", current_content)
        self.assertIn("blah", current_content)

    def _prepare_rss_feeds_file(self, urls):
        os.makedirs(DATA_FILE_PATH)
        with open(RSS_FEED_URLS_FILENAME, "w+") as rss_feed_file:
            for url in urls:
                rss_feed_file.write(url + "\n")
            rss_feed_file.close()
