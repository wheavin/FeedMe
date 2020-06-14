#!/usr/bin/python3

from unittest.mock import patch

from app.feedme_app import feedme_app, RssFeedUrl
from tests.test_app_base import TestAppBase, HTTP_SUCCESS


class TestAppFeedContent(TestAppBase):

    @patch("app.feedme_app.RssFeedUrl")
    def test_load_home_with_valid_url(self, mock_rss_feed_url):
        # Given: a valid RSS Feed config
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

        # When: the root path is loaded
        response = feedme_app.test_client().get("/")

        # Then: the RSS feed content is successfully returned
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"https://www.fiercewireless.com/rss/xml", response.data)
        self.assertIn(b"FeedMe - Home", response.data)

    @patch("feedparser.parse")
    def test_fetch_feed_content_valid_url(self, mock_response):
        # Given a valid RSS feed URL
        rss_feed_url = "https://www.fiercewireless.com/rss/xml"
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link", "author": "Joe Bloggs", "summary": "blah",
                         "published": "123"}]
        }
        # When the RSS feed content is fetched for URL
        response = feedme_app.test_client().get("/content?url=" + rss_feed_url)

        # Then the feed content for URL is returned
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"FierceWireless", response.data)

    @patch("feedparser.parse")
    def test_fetch_feed_content_invalid_url(self, mock_response):
        # Given: an invalid RSS Feed config
        rss_feed_url = "https://www.blahblah.com/rss/xml"
        mock_response.return_value = {
            'entries': [], 'bozo': 1,
            'bozo_exception': TypeError("a bytes-like object is required, not 'RssFeedUrl'", ), 'feed': {}
        }
        # When: the root path is loaded
        response = feedme_app.test_client().get("/content?url=" + rss_feed_url)

        # Then: no RSS feed content is returned
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"No RSS feed content to display", response.data)
