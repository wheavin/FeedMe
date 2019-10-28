#!/usr/bin/python3

import os
from unittest.mock import patch

from pyfakefs import fake_filesystem_unittest

from app import app
from utils.files import get_full_path

DATA_FILE_PATH = get_full_path("data")
RSS_FEED_URLS_FILENAME = get_full_path("data", "rss_feeds.txt")
HTTP_SUCCESS = 200


def _prepare_rss_feeds_file(urls):
    os.makedirs(DATA_FILE_PATH)
    with open(RSS_FEED_URLS_FILENAME, "w+") as rss_feed_file:
        for url in urls:
            rss_feed_file.write(url + "\n")
        rss_feed_file.close()


class TestFeedMeApp(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    @patch("feedparser.parse")
    def test_load_home(self, mock_response):
        # Given: an RSS Feed config
        _prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
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
