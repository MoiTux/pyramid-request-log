import logging
import sys
import time

from pyramid.events import NewResponse, NewRequest
from pyramid.events import subscriber


if sys.version_info[0] < 3:
    str = basestring

log = logging.getLogger(__name__)

unlog_pattern = None
unlog_route = None
authenticated_id = ''


@subscriber(NewRequest)
def log_request(event):
    request = event.request

    if ignore_route(request.path):
        return

    request.pyramid_request_log_start = time.time()

    user = 'UnAuthenticatedUser'
    if request.authenticated_userid:
        user = getattr(request.authenticated_userid,
                       authenticated_id, 'AuthenticatedUser')

    if request.content_type == 'application/json' and request.body:
        try:
            body = request.json_body
            clean(body)
        except Exception:
            body = 'Json error'

        log.info('New request: %s %s (body: %s) (%s: %s)',
                 request.method, request.path_qs, body, authenticated_id, user)
    else:
        log.info('New request: %s %s (%s: %s)',
                 request.method, request.path_qs, authenticated_id, user)


@subscriber(NewResponse)
def log_response(event):
    request = event.request
    response = event.response

    if ignore_route(request.path):
        return

    duration = '{:.3f}'.format(time.time() - request.pyramid_request_log_start)
    extra = {
        'method': request.method,
        'route_url': request.path_qs,
        'status': response.status,
        'duration': duration,
    }

    user = 'UnAuthenticatedUser'
    if request.authenticated_userid:
        user = getattr(request.authenticated_userid,
                       authenticated_id, 'AuthenticatedUser')

    if response.content_type == 'application/json' and response.body:
        try:
            body = response.json_body
            clean(body)
        except Exception:
            body = 'Json error'

        log.info(
            'Response for request: %s %s: HTTPCode: %s, (body: %s) '
            '(%s: %s) (endded in %ss)',
            request.method, request.path_qs, response.status, body,
            authenticated_id, user, duration,
            extra=extra,
        )
    else:
        log.info('Response for request: %s %s: HTTPCode: %s, (%s: %s) '
                 '(endded in %ss)',
                 request.method, request.path_qs, response.status,
                 authenticated_id, user, duration,
                 extra=extra)


def clean(body):
    for key in body:
        if isinstance(key, (dict, list)):
            clean(key)
        elif isinstance(body, dict):
            if isinstance(body[key], (dict, list)):
                clean(body[key])
            elif unlog_pattern and unlog_pattern.match(key):
                body[key] = '*'*6


def ignore_route(route):
    if unlog_route and unlog_route.match(route):
        return True
    return False
