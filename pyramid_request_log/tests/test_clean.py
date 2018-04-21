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

    def test_dict(self):
        request_log.unlog_pattern = re.compile('password')
        data = {
            'authentication': {
                'password': 'Apa$$w0rd',
                'other': 'keep',
            },
            'keep': 'ok',
            'ok': [
                {
                    'too': 'keep',
                },
                {
                    'password': 'to-remove',
                },
            ],
            'bool': True,
        }
        excepted = {
            'authentication': {
                'password': '******',
                'other': 'keep',
            },
            'keep': 'ok',
            'ok': [
                {
                    'too': 'keep',
                },
                {
                    'password': '******',
                },
            ],
            'bool': True,
        }
        request_log.clean(data)
        self.assertEqual(data, excepted)

    def test_mixed_list(self):
        request_log.unlog_pattern = re.compile('password')
        data = [
            1,
            2,
            3,
            {
                'password': 'to-remove',
            },
        ]
        excepted = [
            1,
            2,
            3,
            {
                'password': '******',
            },
        ]
        request_log.clean(data)
        self.assertEqual(data, excepted)

    def test_pattern_in_value(self):
        request_log.unlog_pattern = re.compile('password')
        data = {
            'authentication': {
                'other': 'password',
            },
            'ok': [
                {
                    'too': 'password',
                },
                'password',
            ],
        }
        excepted = {
            'authentication': {
                'other': 'password',
            },
            'ok': [
                {
                    'too': 'password',
                },
                'password',
            ],
        }
        request_log.clean(data)
        self.assertEqual(data, excepted)
