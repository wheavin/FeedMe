#!/usr/bin/python3

from unittest.mock import patch

from parameterized import parameterized

from app.feedme_app import app
from tests.test_app_base import TestAppBase, HTTP_SUCCESS
from user.user import User


@patch("app.feedme_app.db")
class TestAppRegistration(TestAppBase):

    def test_register_with_new_user(self, mock_db):
        # When: a new user is registered
        response = app.test_client().post(
            "/register",
            data=dict(email="bill@email.com", password="test", repeat_password="test", register=True),
            follow_redirects=True
        )
        # Then: the registration is successful
        assert mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Sign In", response.data)

    @parameterized.expand([
        ["Not an email", "not_an_email", b"Invalid email address"],
        ["Empty email", "", b"This field is required"],
        ["Blank email", "  ", b"This field is required"],
        ["Null email", None, b"This field is required"]
    ])
    def test_register_with_invalid_email(self, mock_db, _, invalid_email, expected_error):
        # When: a new user is registered with invalid email
        response = app.test_client().post(
            "/register",
            data=dict(email=invalid_email, password="test", repeat_password="test", register=True),
            follow_redirects=True
        )
        # Then: the registration is not successful
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Register", response.data)
        self.assertIn(expected_error, response.data)

    @patch("user.user_registration.User")
    def test_register_with_already_used_email(self, mock_user, mock_db):
        # Given: a user already existing with email
        mock_user.query.filter_by.first.return_value = User(email="bill@email.com", password="test", authenticated=True)

        # When: a new user is registered with same email
        response = app.test_client().post(
            "/register",
            data=dict(
                email="bill@email.com", password="test", repeat_password="test", register=True),
            follow_redirects=True
        )
        # Then: the registration is not successful
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Register", response.data)
        self.assertIn(b"Email already in use. Please choose a different email", response.data)

    @parameterized.expand([
        ["Empty password", ""],
        ["Blank password", "  "],
        ["Null password", None]
    ])
    def test_register_with_no_password_provided(self, mock_db, _, invalid_password):
        # When: a new user is registered with no password provided
        response = app.test_client().post(
            "/register",
            data=dict(
                email="bill@email.com", password=invalid_password, repeat_password=invalid_password, register=True),
            follow_redirects=True
        )
        # Then: the registration is not successful
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Register", response.data)
        self.assertIn(b"This field is required", response.data)

    def test_register_with_incorrect_repeat_password(self, mock_db):
        # When: a new user is registered
        response = app.test_client().post(
            "/register",
            data=dict(
                email="bill@email.com", password="test", repeat_password="wrong_password", register=True),
            follow_redirects=True
        )
        # Then: the registration is not successful
        assert not mock_db.session.commit.called
        self.assertEqual(HTTP_SUCCESS, response.status_code)
        self.assertIn(b"Register", response.data)
        self.assertIn(b"Field must be equal to password", response.data)
