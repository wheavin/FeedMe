import json


class FileReader:

    def __init__(self, path):
        self.path = path

    def read(self):
        pass


class TextFileReader(FileReader):

    def read(self):
        with open(self.path) as text_file:
            return text_file.read()


class JsonFileReader(FileReader):

    def read(self):
        with open(self.path) as json_file:
            return json.load(json_file)
