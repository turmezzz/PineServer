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
class
if __name__ == '__main__':
    unittest.main()

