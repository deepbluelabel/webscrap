from abc import *
from bs4 import BeautifulSoup as bs

class Scrap(metaclass=ABCMeta):
    def __init__(self, session):
        self._session = session

    def run(self):
        self._load()
        self._parse()
        self._process()

    def _getPage(self, url):
        body = self._session.get(url)
        return bs(body.text, 'html.parser')

    def _postPage(self, url, data):
        return self._session.post(url, data=data)

    def _load(self):
        pass

    def _parse(self):
        pass

    def _process(self):
        pass