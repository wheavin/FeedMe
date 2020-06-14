#!/usr/bin/python3

from unittest.mock import patch

from app.feedme_app import feedme_app, RssFeedUrl
from tests.test_app_base import TestAppBase, HTTP_SUCCESS


class TestAppConfigureRssFeeds(TestAppBase):

    @patch("app.feedme_app.RssFeedUrl")
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

    @patch("app.feedme_app.RssFeedUrl")
    def test_create_rss_feed_url_entry_duplicate(self, mock_rss_feed_url):
        # Given: an already added RSS feed URL
        rss_feed_url = RssFeedUrl()
        rss_feed_url.url = "https://www.fiercewireless.com/rss/xml"
        mock_rss_feed_url.query.filter_by.first.return_value = rss_feed_url
        mock_rss_feed_url.query.all.return_value = [rss_feed_url]

        # When: the RSS feed URL is added again
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

    @patch("app.feedme_app.db")
    @patch("app.feedme_app.RssFeedUrl")
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

    @patch("app.feedme_app.db")
    @patch("app.feedme_app.RssFeedUrl")
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
