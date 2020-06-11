#!/usr/bin/python3
"""
REST endpoints for FeedMe app.
"""

import flask_bcrypt as bcrypt
from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy

from feed import feed
from user.user import User
from user.user_login import LoginForm
from utils.files import get_full_path

DATABASE_FILE = "sqlite:///{}".format(get_full_path("urldatabase.db"))

feedme_app = Flask(__name__)
feedme_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
feedme_app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_FILE
feedme_app.config["SECRET_KEY"] = "7d441f27d441f27567d441f2b6176a"

db = SQLAlchemy(feedme_app)

login_manager = LoginManager()
login_manager.init_app(feedme_app)
login_manager.login_view = "login"


class RssFeedUrl(db.Model):
    """
    DB model for Rss Feed URL.
    """
    url = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)

    def __repr__(self):
        return "<RssFeedUrl: {}>".format(self.url)


@feedme_app.route("/")
def show_feed():
    """
    Displays the RSS Feed item URLs.
    :return: main web page containing RSS feed item URLs.
    """
    print("Loading home page")
    rss_feed_url_entries = RssFeedUrl.query.all()
    rss_feed_urls = [entry.url for entry in rss_feed_url_entries]
    return render_template("index.html", page_title="FeedMe", rss_feed_urls=rss_feed_urls)


@feedme_app.route("/content", methods=["GET"])
def fetch_feed_content():
    """
    Fetches the RSS feed content for a given URL.
    :return: the RSS feed content.
    """
    print("Fetching RSS feed content for " + request.args["url"])
    url = request.args.get("url")
    feed_content = feed.fetch_content_for_feed_url(url)
    return feed_content


@feedme_app.route("/config", methods=["GET", "POST"])
@login_required
def create():
    """
    Adds new RSS feed URL to the database.
    :return: config web page containing updated list of URL entries.
    """
    if request.form:
        if request.form.get("url"):
            rss_feed_url = RssFeedUrl(url=request.form.get("url"))
            print("Adding: " + rss_feed_url.url)

            url_already_added = RssFeedUrl.query.filter_by(url=rss_feed_url.url).first()
            if url_already_added:
                flash("URL already added. Please provide a unique URL")
            else:
                db.session.add(rss_feed_url)
                db.session.commit()
                print("Added RSS feed URL: {}".format(rss_feed_url))
        else:
            flash("Please provide a valid URL")

    urls = RssFeedUrl.query.all()
    return render_template("urlconfig.html", rss_feed_urls=urls)


@feedme_app.route("/update", methods=["POST"])
def update():
    """
    Updates URL for existing RSS feed URL entry.
    :return: config web page containing updated list of URL entries.
    """
    new_url = request.form.get("new_url")
    old_url = request.form.get("old_url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=old_url).first()
    rss_feed_url.url = new_url
    db.session.commit()
    print("Updated RSS feed URL from {} to {}".format(old_url, new_url))
    return redirect("/config")


@feedme_app.route("/delete", methods=["POST"])
def delete():
    """
    Deletes RSS feed URL entry from the database.
    :return: config web page containing updated list of URL entries.
    """
    url = request.form.get("url")
    rss_feed_url = RssFeedUrl.query.filter_by(url=url).first()
    db.session.delete(rss_feed_url)
    db.session.commit()
    print("Deleted RSS feed URL {}".format(url))
    return redirect("/config")


@feedme_app.route("/login", methods=["GET", "POST"])
def login():
    """
    Logs in the user given provided user id and password.
    :return: homepage if login successful, otherwise return login form.
    """
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.get(login_form.email.data)

        if user and bcrypt.check_password_hash(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            user.authenticated = True
            flash("Logged in successfully")
            return redirect(next or "/")

    flash("Log in not successful")
    return render_template("login.html", login_form=login_form)


@feedme_app.route("/logout")
@login_required
def logout():
    """
    Log out the current user.
    :return: the home page.
    """
    logout_user()
    return redirect("/")


@login_manager.user_loader
def user_loader(user_id):
    """
    Returns the associated User object for a given user id.
    :param user_id: email of the user
    :return: the User object
    """
    return User.query.get(user_id)


if __name__ == '__main__':
    feedme_app.run()
