#!/usr/bin/python3

import sys

import flask_bcrypt as bcrypt

from app.feedme_app import feedme_app
from user.user import db, User


def main():
    with feedme_app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print("An admin user already exists!"),
            return

        email = "administrator@feedme.com"
        password = "admin"
        user = User(email=email, password=bcrypt.generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print("Admin user added")


if __name__ == '__main__':
    sys.exit(main())
