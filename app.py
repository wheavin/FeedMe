#!/usr/bin/python3

from flask import Flask, render_template

from feed.feed import Feed

app = Flask(__name__)
rss_feed = Feed()


@app.route("/")
def refresh_feed():
    print("Refreshing RSS feed content")
    feed_content = rss_feed.refresh_content()
    return render_template("index.html", page_title="FeedMe", feed_content=feed_content)


if __name__ == '__main__':
    app.run()
