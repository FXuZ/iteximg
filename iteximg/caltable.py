#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import struct
from iteximg.util import calib_addr_len_parser


class CalibTable():
    def __init__(self, fn: str = "",
                 describer: str = "",
                 unit: str = ""):
        '''
        The initialization of a calibration table
        :Args:
            :fn: str, the file name
            :describer: str, the describer of the cal table in file. It should
            look like "#xxxxx,yyy", where xxxxx is the address and yyy is the
            size, i.e. the number of points in the table
        The calib table region in the file should consists of an array of
        4-byte floats in little endian
        '''
        if describer != "":
            self._populate_calib(fn, describer, unit)
        else:
            self.table = None

        self.unit = unit
        self.__getitem__ = self.table.__getitem__

    def _populate_calib(self, fn: str,
                        describer: str,
                        unit: str):
        addr, length = calib_addr_len_parser(describer)
        with open(fn, 'rb') as f:
            f.seek(addr)
            buffer = f.read(4 * length)
            buffer = struct.unpack_from("<{}f".format(length),
                                        buffer, 0)
            self.table = np.array(buffer, dtype=np.float32)
            # super().__init__(self, buffer, dtype=np.float32)
