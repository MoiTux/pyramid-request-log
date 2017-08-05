from unittest import TestCase

import re

from .. import request_log


class TestClean(TestCase):

    def tearDown(self):
        request_log.unlog_pattern = None

    def test_no_patern(self):
        data = {
            'ok': 'ko',
        }
        excepted = {
            'ok': 'ko',
        }
        request_log.clean(data)
        self.assertEqual(data, excepted)

    def test_patern(self):
        request_log.unlog_pattern = re.compile('ok')
        data = {
            'ok': 'ko',
            'ko': 'ko',
        }
        excepted = {
            'ok': '******',
            'ko': 'ko',
        }
        request_log.clean(data)
        self.assertEqual(data, excepted)

    def test_list(self):
        request_log.unlog_pattern = re.compile('ok')
        data = [
            {
                'ok': 'ko',
            },
            {
                'ko': 'ko',
            },
        ]
        excepted = [
            {
                'ok': '******',
            },
            {
                'ko': 'ko',
            },
        ]
        request_log.clean(data)
        self.assertEqual(data, excepted)
