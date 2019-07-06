"""
Helps resolve file paths in project.
"""
from os.path import join, dirname

MAIN_DIRECTORY = dirname(dirname(__file__))


def get_full_path(*path):
    """
    Gets full path of file.
    :param path:
    :return:
    """
    return join(MAIN_DIRECTORY, *path)
