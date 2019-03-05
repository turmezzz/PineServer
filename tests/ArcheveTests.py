import unittest
from MainApp.tools import send_mail
import os

class ArcheveTests(unittest.TestCase):

    def testArchevesend1(self):
        res = send_mail('dikrivenkov@edu.hse.ru','../files/zips/images.zip')
        self.assertTrue(res)
    def testArchevesend2(self):
        res = send_mail('dikrivenkov@edu.hse.ru', '../files/zips/images.zip')
        self.assertTrue(res)


class MetricsTests(unittest.TestCase):

    def testMaxmetric(self):
        labels = [[{'bottomright': {'x': 602, 'y': 585},
                    'confidence': 0.38619694,
                    'label': 'person',
                    'topleft': {'x': 455, 'y': 334}},
                   {'bottomright': {'x': 636, 'y': 776},
                    'confidence': 0.28718543,
                    'label': 'person',
                    'topleft': {'x': 563, 'y': 281}},
                   {'bottomright': {'x': 623, 'y': 959},
                    'confidence': 0.8782011,
                    'label': 'person',
                    'topleft': {'x': 0, 'y': 207}},
                   {'bottomright': {'x': 631, 'y': 959},
                    'confidence': 0.82520235,
                    'label': 'person',
                    'topleft': {'x': 476, 'y': 295}},
                   {'bottomright': {'x': 225, 'y': 881},
                    'confidence': 0.11298049,
                    'label': 'chair',
                    'topleft': {'x': 4, 'y': 387}}]]


if __name__ == '__main__':
    unittest.main()

