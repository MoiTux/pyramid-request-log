from __future__ import absolute_import

from unittest import TestCase

from pyramid.config import Configurator
from testfixtures import log_capture

from .. import config, request_log


class TestConfig(TestCase):

    def tearDown(self):
        request_log.unlog_pattern = None
        request_log.authenticated_id = ''

    @log_capture()
    def test_no_conf(self, log):
        config.includeme(Configurator())
        log.check(
            (
                'pyramid_request_log.config',
                'WARNING',
                'No pyramid_request_log.pattern found in settings',
            ),
        )
        self.assertIsNone(request_log.unlog_pattern)
        self.assertEqual(request_log.authenticated_id, '')

    @log_capture()
    def test_conf(self, log):
        conf = Configurator()
        conf.registry.settings.update({
            'pyramid_request_log.pattern': '\npassword',
            'pyramid_request_log.ignore_route': '\n/monitoring',
            'pyramid_request_log.authenticated_id': 'me',
        })
        config.includeme(conf)
        log.check(
            (
                'pyramid_request_log.config',
                'INFO',
                "Pyramid-Request-Log will ignore keys: ['password']",
            ),
            (
                'pyramid_request_log.config',
                'INFO',
                "Pyramid-Request-Log will ignore routes: ['/monitoring']",
            ),
        )
        self.assertEqual(request_log.unlog_pattern.pattern, '(password)')
        self.assertEqual(request_log.unlog_route.pattern, '(/monitoring)')
        self.assertEqual(request_log.authenticated_id, 'me')

    @log_capture()
    def test_conf_list(self, log):
        conf = Configurator()
        conf.registry.settings.update({
            'pyramid_request_log.pattern': '\npassword\npwd',
            'pyramid_request_log.ignore_route': '\n^/api.*\n/v5$',
            'pyramid_request_log.authenticated_id': 'me',
        })
        config.includeme(conf)
        log.check(
            (
                'pyramid_request_log.config',
                'INFO',
                "Pyramid-Request-Log will ignore keys: ['password', 'pwd']",
            ),
            (
                'pyramid_request_log.config',
                'INFO',
                "Pyramid-Request-Log will ignore routes: ['^/api.*', '/v5$']",
            ),
        )
        self.assertEqual(request_log.unlog_pattern.pattern, '(password)|(pwd)')
        self.assertEqual(request_log.unlog_route.pattern, '(^/api.*)|(/v5$)')
        self.assertEqual(request_log.authenticated_id, 'me')

    @log_capture()
    def test_conf_empty(self, log):
        conf = Configurator()
        conf.registry.settings.update({
            'pyramid_request_log.pattern': '',
            'pyramid_request_log.ignore_route': '',
            'pyramid_request_log.authenticated_id': 'me',
        })
        config.includeme(conf)
        log.check(
            (
                'pyramid_request_log.config',
                'INFO',
                ('Pyramid-Request-Log will ignore no key: '
                 'variable define but empty'),
            ),
            (
                'pyramid_request_log.config',
                'INFO',
                ('Pyramid-Request-Log will ignore no route: '
                 'variable define but empty'),
            ),
        )
        self.assertIsNone(request_log.unlog_pattern)
        self.assertEqual(request_log.authenticated_id, 'me')
