from unittest import TestCase

import re

from .. import request_log


class TestIgnoreRoute(TestCase):

    def tearDown(self):
        request_log.unlog_route = None

    def test_no_patern(self):
        self.assertFalse(request_log.ignore_route(''))
        self.assertFalse(request_log.ignore_route('42'))
        self.assertFalse(request_log.ignore_route('/stil-ok'))

    def test_patern(self):
        request_log.unlog_route = re.compile('ok')
        self.assertTrue(request_log.ignore_route('ok'))

        self.assertFalse(request_log.ignore_route(''))
        self.assertFalse(request_log.ignore_route('42'))
        self.assertFalse(request_log.ignore_route('/stil-ok'))
