import unittest
from telegram_bot.utils.date_helper import *


class TestDateHelper(unittest.TestCase):

    def test_format_interval(self):
        interval1 = "lun,mar,gio,sab,dom"
        interval2 = "lun,mar,mer,ven,dom"
        interval3 = "dom,sab,ven,lun,mer"
        interval4 = "mer,mar,lun,sab,dom"
        interval5 = "lun"
        interval6 = "lun,mar,mer"
        interval7 = "lun,mar,mer,gio,ven"
        self.assertEqual(format_interval(interval1), "lun,mar,gio,sab,dom")
        self.assertEqual(format_interval(interval2), "lun-mer,ven,dom")
        self.assertEqual(format_interval(interval3), "lun,mer,ven-dom")
        self.assertEqual(format_interval(interval4), "lun-mer,sab,dom")
        self.assertEqual(format_interval(interval5), "lun")
        self.assertEqual(format_interval(interval6), "lun-mer")
        self.assertEqual(format_interval(interval7), "lun-ven")


def benchmark_format_interval():
    interval1 = ["lun", "mar", "gio", "sab", "dom"]
    interval2 = ["lun", "mar", "mer", "ven", "dom"]
    interval3 = ["dom", "sab", "ven", "lun", "mer"]
    interval4 = ["mer", "mar", "lun", "sab", "dom"]
    interval5 = ["lun"]
    interval6 = ["lun", "mar", "mer"]

    format_interval(interval1)
    format_interval(interval2)
    format_interval(interval3)
    format_interval(interval4)
    format_interval(interval6)
    format_interval(interval5)


if __name__ == '__main__':
    from timeit import timeit
    unittest.main()
    print(timeit("benchmark_format_interval()", setup="from __main__ import benchmark_format_interval", number=10000))
