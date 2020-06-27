import sys

from app.feedme_app import db


def main():
    db.create_all()
    print("DB schema created")


if __name__ == '__main__':
    sys.exit(main())
