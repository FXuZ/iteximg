import unittest
from iteximg import util


class TestStrCleaning(unittest.TestCase):
    def test_cleaning(self):
        inputs = [
            "[[a]], [c], \"d\"",
            "[Application],Enconding=UTF-8,Date=\"2/25/2022\",Time=\"1:56:17\"",
            "[bbb],aa=\"1,2,3\""
        ]
        outputs = [
            "[[a]]\n [c]\n \"d\"",
            "[Application]\nEnconding=UTF-8\nDate=\"2/25/2022\"\nTime=\"1:56:17\"",
            "[bbb]\naa=\"1,2,3\""
        ]

        for i, inp in enumerate(inputs):
            self.assertEqual(util.confstr_cleaning(inp), outputs[i])
