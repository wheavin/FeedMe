#!/usr/bin/python3
"""
REST endpoints for FeedMe app.
"""

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from feed.feed import Feed
from utils.files import get_full_path

DATABASE_FILE = "sqlite:///{}".format(get_full_path("urldatabase.db"))

FEEDME_APP = Flask(__name__)
FEEDME_APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
FEEDME_APP.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
FEEDME_APP.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"

DB = SQLAlchemy(FEEDME_APP)


class RssFeedUrl(DB.Model):
    """
    DB model for Rss Feed URL.
    """
    url = DB.Column(DB.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<RssFeedUrl: {}>".format(self.url)


@FEEDME_APP.route("/")
def refresh_feed():
    """
    Refreshes RSS feed content for the configured RSS feed URLs.
    :return: main web page containing updated RSS feed content.
    """
    print("Refreshing RSS feed content")
    rss_feed_url_entries = RssFeedUrl.query.all()
    rss_feed_urls = []
    for entry in rss_feed_url_entries:
        rss_feed_urls.append(entry.url)

    rss_feed = Feed(rss_feed_urls)
    feed_content = rss_feed.refresh_content()
    return render_template("index.html", page_title="FeedMe", feed_content=feed_content)


@FEEDME_APP.route("/config", methods=["GET", "POST"])
def create():
    """
    Adds new RSS feed URL to the database.
    :return: config web page containing updated list of URL entries.
    """
    if request.form:
        if request.form.get("url"):
            rss_feed_url = RssFeedUrl(url=request.form.get("url"))

            url_already_added = RssFeedUrl.query.filter_by(url=rss_feed_url).first()
            if url_already_added:
                flash("URL already added. Please provide a unique URL")
            else:
                DB.session.add(rss_feed_url)
                DB.session.commit()
                print("Added RSS feed URL: {}".format(rss_feed_url))
        else:
            flash("Please provide a valid URL")

    urls = RssFeedUrl.query.all()
    return render_template("urlconfig.html", rss_feed_urls=urls)


@FEEDME_APP.route("/update", methods=["POST"])
def update():
    """
    Updates URL for existing RSS feed URL entry.
    :return: config web page containing updated list of URL entries.
    """
    new_url = request.form.get("new_url")
    old_url = request.form.get("old_url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=old_url).first()
    rss_feed_url.url = new_url
    DB.session.commit()
    print("Updated RSS feed URL from {} to {}".format(old_url, new_url))
    return redirect("/config")


@FEEDME_APP.route("/delete", methods=["POST"])
def delete():
    """
    Deletes RSS feed URL entry from the database.
    :return: config web page containing updated list of URL entries.
    """
    url = request.form.get("url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=url).first()
    DB.session.delete(rss_feed_url)
    DB.session.commit()
    print("Deleted RSS feed URL {}".format(url))
    return redirect("/config")


if __name__ == '__main__':
    FEEDME_APP.run()
