#!/usr/bin/python3

import os

from pyfakefs import fake_filesystem_unittest

from app import app
from utils.files import get_full_path

DATA_FILE_PATH = get_full_path("data")
RSS_FEED_URLS_FILENAME = get_full_path("data", "rss_feeds.txt")


def _prepare_rss_feeds_file(urls):
    os.makedirs(DATA_FILE_PATH)
    with open(RSS_FEED_URLS_FILENAME, "w+") as rss_feed_file:
        for url in urls:
            rss_feed_file.write(url + "\n")
        rss_feed_file.close()


class TestFeedMeApp(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def test_load_home(self):
        _prepare_rss_feeds_file("https://www.fiercewireless.com/rss/xml")
        response = app.test_client().get("/")
        assert response.status_code == 200
        self.assertIn(b"fiercewireless", response.data)
