#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import struct
import numpy as np
from iteximg.itexstatus import ITEXStatus
from iteximg.caltable import CalibTable
from iteximg.util import confstr_cleaning


class ITEX:
    '''
    The container type for ITEX img filesself.
    It contains a struct for the file format.
    '''
    def __init__(self):
        self.file = ''
        self.cntblock = None    # raw control block of 62 bytes
        self.bytes_per_pix = -1  # num bytes for each pix
        self.xsize = -2          # x dim of image
        self.ysize = -1          # y dim of image
        self.csize = -1          # length of comment string

        self.status = None      # status string object
        self.xcalib = None      # calib table object for x
        self.ycalib = None      # calib table object for y
        self.image = None       # The image data
        self.release()

    def load_file(self, fn: str):
        self.file = fn

        with open(fn, "rb") as f:
            self.cntblock = f.read(63)

        self._check_filetype()
        self._populate_meta()
        self._load_comment()
        self._load_data()
        self._load_calib()

    def release(self):
        self.file = ''
        self.cntblock = None    # raw control block of 62 bytes
        self.bytes_per_pix = -1  # num bytes for each pix
        self.xsize = -2          # x dim of image
        self.ysize = -1          # y dim of image
        self.csize = -1          # length of comment string

        self.status = None      # status string object
        self.xcalib = None      # calib table object for x
        self.ycalib = None      # calib table object for y
        self.image = None       # The image data

    def _check_filetype(self):
        if len(self.file) == -1:
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

    def _load_data(self):
        with open(self.file, 'rb') as f:
            f.seek(64 + self.csize)
            dblock = f.read(self.xsize * self.ysize * self.bytes_per_pix)
            dblock = struct.unpack_from("<{}H".format(self.xsize * self.ysize),
                                        dblock,
                                        0)
            self.image = np.array(dblock,
                                  dtype=np.int16)\
                .reshape(self.ysize, self.xsize)
            print(self.image.shape)
            self.image = np.flip(self.image, axis=1)

    def _load_calib(self):
        if self.status is None:
            raise RuntimeError("Image not initialized!"
                               "Please populate status string!")
        sdict = self.status.as_dict()["Scaling"]

        xdescr = sdict["scalingxscalingfile"]
        xunit = sdict["scalingxunit"]
        self.xcalib = CalibTable(self.file, xdescr, xunit)

        ydescr = sdict["scalingyscalingfile"]
        yunit = sdict["scalingyunit"]
        if ydescr == "Focus mode":
            self.ycalib = CalibTable()
            self.ycalib.table = np.arange(self.ysize)
            self.ycalib.__getitem__ = self.ycalib.table.__getitem__
        else:
            self.ycalib = CalibTable(self.file, ydescr, yunit)
