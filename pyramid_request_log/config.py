from __future__ import absolute_import

import logging
import re

from pyramid.settings import aslist

from . import request_log

log = logging.getLogger(__name__)


def includeme(config):
    settings = config.registry.settings

    config.scan('pyramid_request_log.request_log')

    if 'pyramid_request_log.pattern' in settings:
        unlog_pattern = aslist(settings['pyramid_request_log.pattern'])
        if not unlog_pattern:
            log.info('Pyramid-Request-Log will ignore no key: '
                     'variable define but empty')
        else:
            log.info('Pyramid-Request-Log will ignore keys: %s', unlog_pattern)

            re_compile = re.compile('({})'.format(')|('.join(unlog_pattern)))
            request_log.unlog_pattern = re_compile
    else:
        log.warning('No pyramid_request_log.pattern found in settings')

    if 'pyramid_request_log.ignore_route' in settings:
        unlog_route = aslist(settings['pyramid_request_log.ignore_route'])
        if not unlog_route:
            log.info('Pyramid-Request-Log will ignore no route: '
                     'variable define but empty')
        else:
            log.info('Pyramid-Request-Log will ignore routes: %s',
                     unlog_route)

            re_compile = re.compile('({})'.format(')|('.join(unlog_route)))
            request_log.unlog_route = re_compile

    key = 'pyramid_request_log.authenticated_id'
    if key in settings:
        request_log.authenticated_id = settings[key]
