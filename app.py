#!/usr/bin/python3

from flask import Flask

from feed.feed import Feed

app = Flask(__name__)
rss_feed = Feed()


@app.route("/")
def refresh_feed():
    print("Refreshing RSS feed content")
    return rss_feed.refresh_content()


if __name__ == '__main__':
    app.run()
