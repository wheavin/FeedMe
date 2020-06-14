#!/usr/bin/python3

import unittest

from app.feedme_app import feedme_app

HTTP_SUCCESS = 200


class TestAppBase(unittest.TestCase):

    def setUp(self):
        feedme_app.config["TESTING"] = True
        feedme_app.config["LOGIN_DISABLED"] = True
        feedme_app.config["WTF_CSRF_ENABLED"] = False
