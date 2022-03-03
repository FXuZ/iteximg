import unittest
from iteximg.iteximg import ITEX


class TestITEX(unittest.TestCase):
    def setUp(self):
        self.sample_file = 'tests/test_sample.img'
        self.img = ITEX()

    def test_load(self):
        self.img.load_file(self.sample_file)
        self.assertEqual(self.sample_file, self.img.file)
        self.assertEqual(self.img.xsize, 672)
        self.assertEqual(self.img.ysize, 508)
