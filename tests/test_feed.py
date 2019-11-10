#!/usr/bin/python3

import unittest
from unittest.mock import patch

from parameterized import parameterized

from feed.feed import Feed


class TestFeed(unittest.TestCase):
    @patch("feedparser.parse")
    def test_refresh_with_empty_feed(self, mock_response):
        # Given: a feed instance
        rss_feed_urls = ["https://www.fiercewireless.com/rss/xml"]
        obj_under_test = Feed(rss_feed_urls)
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
        rss_feed_urls = ["https://www.fiercewireless.com/rss/xml"]
        obj_under_test = Feed(rss_feed_urls)
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
        rss_feed_urls = ["https://www.fiercewireless.com/rss/xml"]
        obj_under_test = Feed(rss_feed_urls)
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
        rss_feed_urls = ["https://www.fiercewireless.com/rss/xml", "https://www.someotherfeed.com/rss/xml"]
        obj_under_test = Feed(rss_feed_urls)
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

    @parameterized.expand([
        ["Null URL list", None],
        ["Empty URL list", []]
    ])
    def test_refresh_with_empty_rss_feeds(self, _, value):
        # Given: an empty RSS feed URL list
        obj_under_test = Feed(value)

        # When: the feed is refreshed
        feed_content = obj_under_test.refresh_content()

        # Then: no RSS feed content is returned
        self.assertIn("No RSS feed content to display", feed_content)
