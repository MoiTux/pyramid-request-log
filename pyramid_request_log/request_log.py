import logging

from pyramid.events import NewResponse, NewRequest
from pyramid.events import subscriber


log = logging.getLogger(__name__)

unlog_pattern = None
authenticated_id = ''


@subscriber(NewRequest)
def log_request(event):
    request = event.request

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
        if isinstance(key, basestring):
            if unlog_pattern and unlog_pattern.match(key):
                body[key] = '*'*6
        else:
            clean(key)
