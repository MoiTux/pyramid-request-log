import logging
import sys

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
            'Response for request: %s %s: HTTPCode: %s, (body: %s) (%s: %s)',
            request.method, request.path_qs, response.status, body,
            authenticated_id, user,
        )
    else:
        log.info('Response for request: %s %s: HTTPCode: %s, (%s: %s)',
                 request.method, request.path_qs, response.status,
                 authenticated_id, user)


def clean(body):
    for key in body:
        if isinstance(key, (dict, list)):
            clean(key)
        elif isinstance(body, dict) and isinstance(body[key], (dict, list)):
            clean(body[key])
        elif (unlog_pattern and isinstance(key, str) and
              unlog_pattern.match(key)):
            body[key] = '*'*6


def ignore_route(route):
    if unlog_route and unlog_route.match(route):
        return True
    return False
