#!/usr/bin/python3

"""
Contains the RSS feed URLs.
"""


class RssFeedUrls:
    def __init__(self, urls):
        self.urls = urls

    def get_urls(self):
        return ["https://www.fiercewireless.com/rss/xml"] if self.urls is None else self.urls
