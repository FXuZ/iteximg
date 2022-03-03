#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser


class ITEXStatus(configparser.ConfigParser):
    def __init__(self, status_string):
        super().__init__()
        self.read_string(status_string)
        # print(self._sections)

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = {}
            for o in self.options(k):
                d[k][o] = self.get(k, o)
        return d
