#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
from iteximg.itexstatus import ITEXStatus
from iteximg.util import confstr_cleaning


class ITEX:
    '''
    The container type for ITEX img filesself.
    It contains a struct for the file format.
    '''
    def __init__(self):
        self.release()

    def load_file(self, fn: str):
        self.file = fn

        with open(fn, "rb") as f:
            self.cntblock = f.read(64)

        self._check_filetype()
        self._populate_meta()
        self._load_comment()
        self._load_data()
        self._load_calib()

    def release(self):
        self.file = ''
        self.cntblock = None
        self.bytes_per_pix = 1  # num bytes for each pix
        self.xsize = 0          # x dim of image
        self.ysize = 0          # y dim of image
        self.csize = 0          # length of comment string
        self.status = None      # status string object
        self.xcalib = None      # calib table object for x
        self.ycalib = None      # calib table object for y
        self.image = None       # The image data

    def _check_filetype(self):
        if len(self.file) == 0:
            return False
        # Check file type
        t1, t2 = struct.unpack_from("2c", self.cntblock, 0)
        return (t1 == b'I') and (t2 == b'M')

    def _populate_meta(self):
        self.csize, self.xsize, self.ysize\
            = struct.unpack_from("<3H", self.cntblock, 2)
        (fmt,) = struct.unpack_from("<H", self.cntblock, 12)

        if fmt == 0:
            self.bytes_per_pix = 1
        elif fmt == 2:
            self.bytes_per_pix = 2
        elif fmt == 3:
            self.bytes_per_pix = 4
        else:
            raise ValueError("Parsing error: File Format should be 0, 2, or 3")

    def _load_comment(self):
        with open(self.file, 'rb') as f:
            f.seek(64)
            sstr = f.read(self.csize)
            sstr = confstr_cleaning(sstr.decode())
            self.status = ITEXStatus(sstr.replace("[", "\n["))
        # print(self.status.as_dict()["Scaling"])
        # self.status =

    def _load_data(self):
        pass

    def _load_calib(self):
        pass
