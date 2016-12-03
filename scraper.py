import csv
import requests
from lxml import html


class Csv:
    def __init__(self, path, encoding=None, **params):
        self.path = path
        self.writer = csv.writer(
            open(self.path, "a+", encoding=encoding), **params)

        self.reader = csv.DictReader(
            open(self.path, "r", encoding=encoding), **params)

    @property
    def rows(self):
        return self.reader

    def write(self, *row):
        self.writer.writerow(*row)


class Env:
    def __init__(self, proxy=None, headers=None, verify=True):
        self.s = requests.Session()
        self.s.verify = verify

        if headers is not None:
            self.s.headers.update(headers)

        if proxy is not None:
            self.s.proxies.update(proxy)

    def get(self, url, params=None):
        return self.s.get(url, params=params)

    def post(self, url, data=None):
        return self.s.post(url, data=data)

    def get_dom(self, url, encoding=None):
        r = self.s.get(url)

        if encoding is not None:
            r.encoding = encoding

        return html.fromstring(r.text)

    def html_to_dom(self, html_string):
        return html.fromstring(html_string)
