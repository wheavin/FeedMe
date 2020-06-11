#!/usr/bin/python3

from urllib.parse import urlparse, urljoin

from flask import request


def is_safe_url(target):
    """
    Validates if URL containing "next" variable is safe.
    This is to avoid malicious redirects.
    :param target: "next" variable.
    :return: True if the url is safe, False otherwise.
    """
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc
