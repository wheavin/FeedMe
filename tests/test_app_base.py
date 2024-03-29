#!/usr/bin/python3

import unittest

from app.feedme_app import app

HTTP_SUCCESS = 200


class TestAppBase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["LOGIN_DISABLED"] = True
        app.config["WTF_CSRF_ENABLED"] = False
