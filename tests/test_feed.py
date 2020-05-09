#!/usr/bin/python3

import unittest
from unittest.mock import patch

from parameterized import parameterized

from feed import feed


class TestFeed(unittest.TestCase):

    @patch("feedparser.parse")
    def test_fetch_content_for_feed_url_with_single_entry(self, mock_response):
        # Given: a valid RSS feed URL
        rss_feed_url = "https://www.fiercewireless.com/rss/xml"
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"}]
        }

        # When: the feed content is fetched for url
        feed_content = feed.fetch_content_for_feed_url(rss_feed_url)

        # Then: the feed content is returned successfully
        self.assertIn("<h2>FierceWireless</h2>"
                      "<p>blah</p>"
                      "<h3>Some Entry Title</h3>"
                      "<p><a href=\"some link\" target=\"_blank\">some link</a></p>"
                      "<p>blah</p>"
                      "<p>123 - Joe Bloggs</p>",
                      feed_content)

    @patch("feedparser.parse")
    def test_fetch_content_for_feed_url_with_multiple_entries(self, mock_response):
        # Given: a valid RSS feed URL
        rss_feed_url = "https://www.fiercewireless.com/rss/xml"
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"},
                        {"title": "Another Entry Title", "link": "some link", "author": "Joe Smith", "summary": "blah",
                         "published": "123"}]
        }
        # When: the feed content is fetched for url
        feed_content = feed.fetch_content_for_feed_url(rss_feed_url)

        # Then: the feed content is returned successfully
        self.assertIn("<h2>FierceWireless</h2>"
                      "<p>blah</p>"
                      "<h3>Some Entry Title</h3>"
                      "<p><a href=\"some link\" target=\"_blank\">some link</a></p>"
                      "<p>blah</p>"
                      "<p>123 - Joe Bloggs</p>"
                      "\n\n"
                      "<h3>Another Entry Title</h3>"
                      "<p><a href=\"some link\" target=\"_blank\">some link</a></p>"
                      "<p>blah</p>"
                      "<p>123 - Joe Smith</p>",
                      feed_content)

    @parameterized.expand([
        ["Invalid RSS feed URL", "https://www.notarealfeed.com"],
        ["Empty RSS feed URL", ""],
        ["Null RSS feed URL", None]
    ])
    def test_fetch_content_for_feed_url_with_invalid_url(self, _, value):
        # When: the feed content is fetched for url
        feed_content = feed.fetch_content_for_feed_url(value)

        # Then: no RSS feed content is returned
        self.assertIn("No RSS feed content to display", feed_content)
