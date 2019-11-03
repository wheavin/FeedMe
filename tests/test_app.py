#!/usr/bin/python3

import unittest
from unittest.mock import patch

from app import app
from utils.files import get_full_path

DATA_FILE_PATH = get_full_path("data")
RSS_FEED_URLS_FILENAME = get_full_path("data", "rss_feeds.txt")
TEMPLATES_DIR = get_full_path("templates")
INDEX_HTML_FILENAME = get_full_path("templates", "index.html")
HTTP_SUCCESS = 200


class TestFeedMeApp(unittest.TestCase):
    @patch("feedparser.parse")
    def test_load_home(self, mock_response):
        # Given: an RSS Feed config
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"}]
        }
        # When: the root path is loaded
        response = app.test_client().get("/")

        # Then: the RSS feed content is successfully returned
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"FierceWireless", response.data)
