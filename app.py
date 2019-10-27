#!/usr/bin/python3

from flask import Flask

from feed.feed import Feed
from utils.file_reader import TextFileReader
from utils.files import get_full_path

RSS_FEED_CONTENT_FILENAME = get_full_path("data", "rss_feed_content.txt")

app = Flask(__name__)
rss_feed = Feed()


@app.route("/")
def refresh_feed():
    print("Refreshing RSS feed content")
    rss_feed.refresh_content()
    file_reader = TextFileReader(RSS_FEED_CONTENT_FILENAME)
    return file_reader.read()


if __name__ == '__main__':
    app.run()
