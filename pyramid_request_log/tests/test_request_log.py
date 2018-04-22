import re
import sys
import mock
from unittest import TestCase
from testfixtures import log_capture

from .. import request_log
from .base import get_app


class TestRequestLog(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = get_app()

    @classmethod
    def tearDown(cls):
        request_log.unlog_pattern = None
        request_log.unlog_route = None

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
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
                '(username: UnAuthenticatedUser) (endded in 0.000s)',
            ),
        )

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
    @log_capture()
    def test_unauthenticated_json(self, log):
        data = {'some': 'data'}
        res = self.app.post_json('/', params=data,
                                 headers={'content-type': 'application/json'})
        self.assertEqual(res.json, data)
        if sys.version_info[0] < 3:
            logged_body = "{u'some': u'data'}"
        else:
            logged_body = "{'some': 'data'}"
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                "New request: POST / (body: {}) "
                '(username: UnAuthenticatedUser)'.format(logged_body),
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: POST /: HTTPCode: 200 OK, (body: {}) '
                '(username: UnAuthenticatedUser) (endded in 0.000s)'
                ''.format(logged_body),
            ),
        )

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
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
                '(username: MoiTux) (endded in 0.000s)',
            ),
        )

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
    @log_capture()
    def test_authenticated_bad_json(self, log):
        data = "{'bad': 'json', }"
        res = self.app.post('/', params=data,
                            headers={'X-Authenticated-User': '',
                                     'content-type': 'application/json'})
        self.assertEqual(res.text, data)
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
                "(body: Json error) (username: MoiTux) (endded in 0.000s)",
            ),
        )

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
    @log_capture()
    def test_authenticated_nochange(self, log):
        request_log.unlog_pattern = re.compile('some')
        data = {'some': 'data'}
        res = self.app.post_json('/', params=data,
                                 headers={'X-Authenticated-User': '',
                                          'content-type': 'application/json'})
        self.assertEqual(res.json, data)
        if sys.version_info[0] < 3:
            logged_body = "{u'some': '******'}"
        else:
            logged_body = "{'some': '******'}"
        log.check(
            (
                'pyramid_request_log.request_log',
                'INFO',
                "New request: POST / (body: {}) "
                "(username: MoiTux)".format(logged_body),
            ),
            (
                'pyramid_request_log.request_log',
                'INFO',
                'Response for request: POST /: HTTPCode: 200 OK, '
                '(body: {}) (username: MoiTux) (endded in 0.000s)'
                ''.format(logged_body),
            ),
        )

    @mock.patch('pyramid_request_log.request_log.time.time', lambda: 0)
    @log_capture()
    def test_ignore_route(self, log):
        request_log.unlog_route = re.compile('/')
        data = {'some': 'data'}
        res = self.app.post_json('/', params=data,
                                 headers={'X-Authenticated-User': '',
                                          'content-type': 'application/json'})
        self.assertEqual(res.json, data)
        log.check()
