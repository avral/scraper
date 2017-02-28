import os
import csv
from lxml import html

import requests


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
        self.writer.writerow(row)

    def write_if_empty(self, *row):
        if os.stat(self.path).st_size == 0:
            self.write(*row)


class Env(requests.Session):
    tor_controller_port = 9051

    def __init__(self, use_tor=False, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.verify = False

        if use_tor:
            self.proxies = {'http':  'socks5://127.0.0.1:9050',
                            'https': 'socks5://127.0.0.1:9050'}

    def get_dom(self, url, params=None, encoding=None):
        self.r = self.get(url, params=params)
        self.r.encoding = encoding

        return self.html_to_dom(self.r.text)

    def post_dom(self, url, data=None, encoding=None):
        self.r = self.post(url, data=data)
        self.r.encoding = encoding

        return self.html_to_dom(self.r.text)

    def html_to_dom(self, html_string):
        return html.fromstring(html_string)

    def change_tor_ip(self):
        try:
            from stem import Signal
            from stem.control import Controller
        except ModuleNotFoundError:
            raise Exception('Tor lib not found. Install by "pip install stem"')

        with Controller.from_port(port=self.tor_controller_port) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)

        self.close()
