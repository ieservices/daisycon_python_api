import logging
import os
import unittest

from src.dasicon_api import DaisyconApi


class TestDaisyconApi(unittest.TestCase):
    def setUp(self):
        # set up logging
        logging.root.handlers = []
        logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

        logging.info('Setiting up DaisyconApi')
        username = os.environ.get('DASIYCON_USERNAME')
        password = os.environ.get('DASIYCON_PASSWORD')
        publisher_id = os.environ.get('DASIYCON_PUBLISHER_ID')

        self.api = DaisyconApi(username, password, publisher_id)

    def test_get_publisher_programs(self):
        pages_data, value_count = self.api.get_publisher_programs(page=1, per_page=1)
        self.assertGreater(len(pages_data), 0)
        self.assertGreater(value_count, 1)
