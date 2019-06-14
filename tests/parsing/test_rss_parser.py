import json
import os
import unittest
from unittest.mock import patch

from parameterized import parameterized

from parser.rss_parser import RssUrlParser, RssParserError

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'data/rss_sample.json')


class TestRssParsing(unittest.TestCase):

    @patch('feedparser.parse')
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
    @patch('feedparser.parse')
    def test_parse_for_invalid_response(self, _, value, mock_response):
        # Given: an RSS feed URL to be parsed
        url = "https://www.fiercewireless.com/rss/xml"
        obj_under_test = RssUrlParser(url)
        mock_response.return_value = value

        # When: the URL is parsed
        with self.assertRaises(RssParserError) as error:
            obj_under_test.parse()
        self.assertIn("Invalid response returned for URL", error.exception.message)


class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path) as json_file:
            return json.load(json_file)
