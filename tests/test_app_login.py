#!/usr/bin/python3

from unittest.mock import patch

from parameterized import parameterized

from app.feedme_app import app
from tests.test_app_base import TestAppBase, HTTP_SUCCESS
from user.user import User


class TestAppLogin(TestAppBase):

    @patch("app.feedme_app.db")
    @patch("app.feedme_app.User")
    def test_login_with_valid_credentials(self, mock_user, mock_db):
        # Given: a registered user
        registered_user = User(email="bill@email.com", authenticated=True)
        registered_user.set_password("test")
        mock_user.query.get.return_value = registered_user

        # When: valid login credentials are provided
        response = app.test_client().post(
            "/login",
            data=dict(email="bill@email.com", password="test", remember_me=False, login=True),
            follow_redirects=True
        )
        # Then: the user is successfully logged in
        assert mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"FeedMe - Home", response.data)

    @parameterized.expand([
        ["Wrong password", "wrong_password"],
        ["Empty password", ""],
        ["Blank password", "  "],
        ["Null password", None]
    ])
    @patch("app.feedme_app.db")
    @patch("app.feedme_app.User")
    def test_login_with_invalid_password(self, _, invalid_password, mock_user, mock_db):
        # Given: a registered user
        registered_user = User(email="bill@email.com", authenticated=True)
        registered_user.set_password("test")
        mock_user.query.get.return_value = registered_user

        # When: login credentials are provided with invalid password
        response = app.test_client().post(
            "/login",
            data=dict(email="bill@email.com", password=invalid_password, remember_me=False, login=True),
            follow_redirects=True
        )
        # Then: the user is not logged in
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"FeedMe - Login", response.data)

    @parameterized.expand([
        ["Non-registered email", "bill@email.com"],
        ["Empty email", ""],
        ["Blank email", "  "],
        ["Null email", None]
    ])
    @patch("app.feedme_app.db")
    @patch("app.feedme_app.User")
    def test_login_with_invalid_user(self, _, invalid_email, mock_user, mock_db):
        # Given: the user is not registered
        mock_user.query.get.return_value = None

        # When: login credentials are provided with invalid user
        response = app.test_client().post(
            "/login",
            data=dict(email=invalid_email, password="test", remember_me=False, login=True),
            follow_redirects=True
        )
        # Then: the user is not logged in
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"FeedMe - Login", response.data)
