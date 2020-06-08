#!/usr/bin/python3

import unittest
from unittest.mock import patch

from app import feedme_app, RssFeedUrl

HTTP_SUCCESS = 200


class TestFeedMeApp(unittest.TestCase):

    @patch("app.RssFeedUrl")
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

    @patch("app.RssFeedUrl")
    def test_create_rss_feed_url_entry(self, mock_rss_feed_url):
        # Given: an new RSS feed URL
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

        # When: a new RSS feed URL is added
        response = feedme_app.test_client().post(
            "/config",
            data=dict(url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the config page is reloaded with new entry
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"https://www.fiercewireless.com/rss/xml", response.data)

    @patch("app.RssFeedUrl")
    def test_create_rss_feed_url_entry_duplicate(self, mock_rss_feed_url):
        # Given: an new RSS feed URL
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.filter_by.first.return_value = rss_feed_url
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

        # When: a new RSS feed URL is added
        response = feedme_app.test_client().post(
            "/config",
            data=dict(url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the config page is reloaded with new entry
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"https://www.fiercewireless.com/rss/xml", response.data)

        # When: the same RSS feed URL is added again
        response = feedme_app.test_client().post(
            "/config",
            data=dict(url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the entry will not be added again
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"URL already added. Please provide a unique URL", response.data)

    def test_create_rss_feed_url_entry_with_empty_data(self):
        # When: a blank RSS feed URL is added
        response = feedme_app.test_client().post(
            "/config",
            data=dict(url=""),
            follow_redirects=True
        )
        # Then: no entry will be added
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Please provide a valid URL", response.data)

    @patch("app.db")
    @patch("app.RssFeedUrl")
    def test_update_rss_feed_url_entry(self, mock_rss_feed_url, mock_db):
        # Given: an RSS feel URL entry
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.filter_by.first.return_value = rss_feed_url

        # When: the RSS feed URL entry is updated
        response = feedme_app.test_client().post(
            "/update",
            data=dict(
                new_url="https://www.someothersite.com/rss/xml", old_url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the database has been updated with the changed entry
        assert mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)

    @patch("app.db")
    @patch("app.RssFeedUrl")
    def test_delete_rss_feed_url_entry(self, mock_rss_feed_url, mock_db):
        # Given: an RSS feel URL entry
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.filter_by.first.return_value = rss_feed_url

        # When: the RSS feed URL entry is deleted
        response = feedme_app.test_client().post(
            "/delete",
            data=dict(url="https://www.fiercewireless.com/rss/xml"),
            follow_redirects=True
        )
        # Then: the database has been updated with the removed entry
        assert mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
