from __future__ import absolute_import

import re
from unittest import TestCase
from testfixtures import log_capture

from .. import request_log
from .base import get_app


class TestRequestLog(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()

    @log_capture()
    def test_unauthenticated_no_json(self, log):
        self.app.get('/')
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                'New request: GET / (username: UnAuthenticatedUser)',
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: GET /: HTTPCode: 200 OK, '
                '(username: UnAuthenticatedUser)',
            ),
        )

    @log_capture()
    def test_unauthenticated_json(self, log):
        data = {'some': 'data'}
        res = self.app.post_json('/', params=data,
                                 headers={'content-type': 'application/json'})
        self.assertEqual(res.json, data)
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                "New request: POST / (body: {u'some': u'data'}) "
                '(username: UnAuthenticatedUser)',
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: POST /: HTTPCode: 200 OK, '
                "(body: {u'some': u'data'}) (username: UnAuthenticatedUser)",
            ),
        )

    @log_capture()
    def test_authenticated_no_json(self, log):
        self.app.get('/', headers={'X-Authenticated-User': ''})
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                'New request: GET / (username: MoiTux)',
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: GET /: HTTPCode: 200 OK, '
                '(username: MoiTux)',
            ),
        )

    @log_capture()
    def test_authenticated_bad_json(self, log):
        data = "{'bad': 'json', }"
        res = self.app.post('/', params=data,
                            headers={'X-Authenticated-User': '',
                                     'content-type': 'application/json'})
        self.assertEqual(res.body, data)
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                "New request: POST / (body: Json error) "
                '(username: MoiTux)',
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: POST /: HTTPCode: 200 OK, '
                "(body: Json error) (username: MoiTux)",
            ),
        )

    @log_capture()
    def test_authenticated_nochange(self, log):
        request_log.unlog_pattern = re.compile('some')
        data = {'some': 'data'}
        res = self.app.post_json('/', params=data,
                                 headers={'X-Authenticated-User': '',
                                          'content-type': 'application/json'})
        self.assertEqual(res.json, data)
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                "New request: POST / (body: {u'some': '******'}) "
                '(username: MoiTux)',
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: POST /: HTTPCode: 200 OK, '
                "(body: {u'some': '******'}) (username: MoiTux)",
            ),
        )
        request_log.unlog_pattern = None
