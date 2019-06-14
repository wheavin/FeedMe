import json
import os
import unittest
from unittest.mock import patch

from parameterized import parameterized

from parser.rss_channel import RssItemError
from parser.rss_parser import RssUrlParser, RssParserError

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'data/rss_sample.json')


class TestRssParsing(unittest.TestCase):

    @patch("feedparser.parse")
    def test_parse_rss(self, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)

        test_data = FileReader(TESTDATA_FILENAME)
        mock_response.return_value = test_data.read()

        # When: the URL is parsed
        rss_channel = obj_under_test.parse()

        # Then: the channel details are returned
        self.assertEqual("FierceWireless", rss_channel.title)
        self.assertEqual(url, rss_channel.url)

        # And: the Item details are returned
        self.assertEqual(2, len(rss_channel.rss_items))
        first_item = rss_channel.rss_items[0]
        self.assertIn("Industry Voices—Pongratz", first_item.title)
        self.assertEqual("Stefan Pongratz", first_item.author)

    @patch("feedparser.parse")
    def test_parse_rss_with_no_entries(self, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)
        mock_response.return_value = {
            "feed": {"title": "FierceWireless", "link": "some link", "description": "blah"}, "entries": []
        }
        # When: the URL is parsed
        rss_channel = obj_under_test.parse()

        # Then: the channel details are returned
        self.assertEqual("FierceWireless", rss_channel.title)

        # And: the Item details are empty
        self.assertEqual(0, len(rss_channel.rss_items))

    @parameterized.expand([
        ["Empty URL", ""],
        ["Blank URL", "  "],
        ["Null URL", None]
    ])
    def test_parse_for_invalid_url(self, _, value):
        # Given: an empty RSS feed URL to be parsed
        obj_under_test = RssUrlParser(value)

        # When: the URL is parsed
        with self.assertRaises(RssParserError) as error:
            obj_under_test.parse()
        self.assertIn("Error parsing for URL", str(error.exception))

    @parameterized.expand([
        ["Empty response dict", {}],
        ["Empty response String", ""],
        ["Null response", None]
    ])
    @patch("feedparser.parse")
    def test_parse_for_invalid_response(self, _, value, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)
        mock_response.return_value = value

        # When: the URL is parsed
        with self.assertRaises(RssParserError) as error:
            obj_under_test.parse()
        self.assertIn("Invalid response returned for URL", error.exception.message)

    @parameterized.expand([
        ["No feed element", {"entries": []}],
        ["No title element", {"feed": {"language": "en"}}],
        ["No link element", {"feed": {"title": "Some Title"}}],
        ["No description element", {"feed": {"title": "Some Title", "link": "some link"}}],
        ["No entries elements", {"feed": {"title": "Some Title", "link": "some link", "description": "blah"}}]
    ])
    @patch("feedparser.parse")
    def test_parse_for_invalid_rss_channel(self, _, value, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)
        mock_response.return_value = value

        # When: the URL is parsed
        with self.assertRaises(RssParserError) as error:
            obj_under_test.parse()
        self.assertIn("Invalid RSS channel data", error.exception.message)

    @parameterized.expand([
        ["No entry title element", {
            "feed": {"title": "Some Title", "link": "some link", "description": "blah"},
            "entries": [{"id": 1}]
        }],
        ["No entry link element", {
            "feed": {"title": "Some Title", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title"}]
        }],
        ["No author element", {
            "feed": {"title": "Some Title", "link": "some link", "description": "blah"},
            "entries": [{"title": "Some Entry Title", "link": "some link"}]
        }]
    ])
    @patch("feedparser.parse")
    def test_parse_for_invalid_rss_channel_entries(self, _, value, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)
        mock_response.return_value = value

        # When: the URL is parsed
        with self.assertRaises(RssItemError) as error:
            obj_under_test.parse()
        self.assertIn("Invalid RSS channel entry data", error.exception.message)


class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as json_file:
            return json.load(json_file)
