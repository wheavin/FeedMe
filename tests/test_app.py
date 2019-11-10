#!/usr/bin/python3

import unittest
from unittest.mock import patch

from app import app, RssFeedUrl

HTTP_SUCCESS = 200


class TestFeedMeApp(unittest.TestCase):

    @patch("feedparser.parse")
    @patch("app.RssFeedUrl")
    def test_load_home_with_valid_url(self, mock_rss_feed_url, mock_response):
        # Given: a valid RSS Feed config
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

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

    @patch("feedparser.parse")
    def test_load_home_with_no_valid_urls(self, mock_response):
        # Given: an invalid RSS Feed config
        mock_response.return_value = {
            'entries': [], 'bozo': 1,
            'bozo_exception': TypeError("a bytes-like object is required, not 'RssFeedUrl'", ), 'feed': {}
        }
        # When: the root path is loaded
        response = app.test_client().get("/")

        # Then: no RSS feed content is returned
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"No RSS feed content to display", response.data)

    @patch("app.db")
    @patch("app.RssFeedUrl")
    def test_create_rss_feed_url_entry(self, mock_rss_feed_url, mock_db):
        # Given: an new RSS feed URL
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

        # When: a new RSS feed URL is added
        response = app.test_client().post(
            "/config",
            data=dict(url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the config page is reloaded with new entry
        assert mock_db.session.add.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"https://www.fiercewireless.com/rss/xml", response.data)

    def test_create_rss_feed_url_entry_with_empty_data(self):
        # When: a blank RSS feed URL is added
        response = app.test_client().post(
            "/config",
            data=dict(url=""),
            follow_redirects=True
        )
        # Then: no entry will be added
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Please provide a valid URL", response.data)
