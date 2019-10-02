#!/usr/bin/python3

import unittest


def create_suite():
    loader = unittest.TestLoader()
    return loader.discover('tests')


if __name__ == '__main__':
    suite = create_suite()

    runner = unittest.TextTestRunner()
    runner.run(suite)
