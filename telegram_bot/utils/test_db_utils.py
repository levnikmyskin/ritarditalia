import unittest
from telegram_bot.utils.db_utils import *
from config import *


class TestDbUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
