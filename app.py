#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from feed.feed import Feed
from utils.files import get_full_path

database_file = "sqlite:///{}".format(get_full_path("urldatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"

db = SQLAlchemy(app)


class RssFeedUrl(db.Model):
    url = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<RssFeedUrl: {}>".format(self.url)


@app.route("/")
def refresh_feed():
    print("Refreshing RSS feed content")
    rss_feed_url_entries = RssFeedUrl.query.all()
    rss_feed_urls = []
    for entry in rss_feed_url_entries:
        rss_feed_urls.append(entry.url)

    rss_feed = Feed(rss_feed_urls)
    feed_content = rss_feed.refresh_content()
    return render_template("index.html", page_title="FeedMe", feed_content=feed_content)


@app.route("/config", methods=["GET", "POST"])
def create():
    if request.form:
        if request.form.get("url"):
            rss_feed_url = RssFeedUrl(url=request.form.get("url"))
            db.session.add(rss_feed_url)
            db.session.commit()
            print("Added RSS feed URL: {}".format(rss_feed_url))
        else:
            flash("Please provide a valid URL")

    urls = RssFeedUrl.query.all()
    return render_template("urlconfig.html", rss_feed_urls=urls)


@app.route("/update", methods=["POST"])
def update():
    new_url = request.form.get("new_url")
    old_url = request.form.get("old_url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=old_url).first()
    rss_feed_url.url = new_url
    db.session.commit()
    print("Updated RSS feed URL from {} to {}".format(old_url, new_url))
    return redirect("/config")


@app.route("/delete", methods=["POST"])
def delete():
    url = request.form.get("url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=url).first()
    db.session.delete(rss_feed_url)
    db.session.commit()
    print("Deleted RSS feed URL {}".format(url))
    return redirect("/config")


if __name__ == '__main__':
    app.run()
