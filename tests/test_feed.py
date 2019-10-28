#!/usr/bin/python3

import os
from unittest.mock import patch

from pyfakefs import fake_filesystem_unittest

from feed.feed import Feed, RssFeedError
from utils.files import get_full_path

DATA_FILE_PATH = get_full_path("data")
RSS_FEED_URLS_FILENAME = get_full_path("data", "rss_feeds.txt")


def _prepare_rss_feeds_file(urls):
    os.makedirs(DATA_FILE_PATH)
    with open(RSS_FEED_URLS_FILENAME, "w+") as rss_feed_file:
        for url in urls:
            rss_feed_file.write(url + "\n")
        rss_feed_file.close()


class TestFeed(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    @patch("feedparser.parse")
    def test_refresh_with_empty_feed(self, mock_response):
        # Given: a feed instance
        _prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
        obj_under_test = Feed()
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"}, "entries": []
        }
        # When: the feed is refreshed
        feed_content = obj_under_test.refresh_content()

        # Then: the feed contents have been returned
        self.assertIn("FierceWireless", feed_content)
        self.assertIn("some link", feed_content)
        self.assertIn("blah", feed_content)
        self.assertIn("RSS feed is empty", feed_content)

    @patch("feedparser.parse")
    def test_refresh_with_single_feed_content(self, mock_response):
        # Given: a feed instance
        _prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
        obj_under_test = Feed()
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"}]
        }
        # When: the feed is refreshed
        feed_content = obj_under_test.refresh_content()

        # Then: the feed contents have been updated
        self.assertIn("FierceWireless", feed_content)
        self.assertIn("some link", feed_content)
        self.assertIn("blah", feed_content)
        self.assertIn("Some Entry Title", feed_content)
        self.assertIn("Joe Bloggs", feed_content)

    @patch("feedparser.parse")
    def test_refresh_with_multiple_feed_content(self, mock_response):
        # Given: a feed instance
        _prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
        obj_under_test = Feed()
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"},
                        {"title": "Another Entry Title", "link": "some link", "author": "Joe Smith", "summary": "blah",
                         "published": "123"}]
        }
        # When: the feed is refreshed
        feed_content = obj_under_test.refresh_content()

        # Then: the feed contents have been updated
        self.assertIn("FierceWireless", feed_content)
        self.assertIn("some link", feed_content)
        self.assertIn("blah", feed_content)
        self.assertIn("Some Entry Title", feed_content)
        self.assertIn("Joe Bloggs", feed_content)
        self.assertIn("Another Entry Title", feed_content)
        self.assertIn("Joe Smith", feed_content)

    @patch("feedparser.parse")
    def test_refresh_with_multiple_urls(self, mock_response):
        # Given: two feed instances
        _prepare_rss_feeds_file(["https://www.fiercewireless.com/rss/xml", "https://www.notarealsite.com/rss/xml"])
        obj_under_test = Feed()
        mock_response.side_effect = [{
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [
                {"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                 "published": "123"},
                {"title": "Another Entry Title", "link": "some link", "author": "Joe Smith", "summary": "blah",
                 "published": "123"}]
        }, {
            "feed": {"title": "NotARealSite", "link": "some other link", "description": "lalala"},
            "entries": [
                {"title": "Something interesting", "link": "some link", "author": "Joey Baloni", "summary": "blah",
                 "published": "123"},
                {"title": "Something else", "link": "some link", "author": "Joey Baloni", "summary": "blah",
                 "published": "123"}]
        }]
        # When: the feed is refreshed
        feed_content = obj_under_test.refresh_content()

        # Then: the feed contents have been updated
        self.assertIn("FierceWireless", feed_content)
        self.assertIn("some link", feed_content)
        self.assertIn("Some Entry Title", feed_content)
        self.assertIn("Joe Bloggs", feed_content)

        self.assertIn("NotARealSite", feed_content)
        self.assertIn("some other link", feed_content)
        self.assertIn("Something interesting", feed_content)
        self.assertIn("Joey Baloni", feed_content)

    def test_refresh_with_empty_rss_feeds_file(self):
        # Given: an empty RSS feeds file
        _prepare_rss_feeds_file([])
        obj_under_test = Feed()

        # When: the feed is refreshed
        with self.assertRaises(RssFeedError) as error:
            obj_under_test.refresh_content()

        # Then: an error message is given
        self.assertIn("No RSS feed URLs found", error.exception.message)

    def test_refresh_with_no_rss_feeds_file(self):
        # When: the feed is created with no RSS feeds file
        with self.assertRaises(RssFeedError) as error:
            Feed()

        # Then: an error message is given
        self.assertIn("No RSS feed file found", error.exception.message)
