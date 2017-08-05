from __future__ import absolute_import

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.interfaces import IAuthenticationPolicy
from pyramid.interfaces import IAuthorizationPolicy
from webtest import TestApp
from zope.interface import implementer

from .. import request_log


def hello_world(request):
    if request.content_type == 'application/json':
        return Response(request.body, content_type='application/json')
    return Response('<body><h1>Hello World!</h1></body>')


class AuthenticatedUser(object):

    @property
    def username(self):
        return 'MoiTux'


@implementer(IAuthenticationPolicy)
class AuthenticationPolicy(object):

    def authenticated_userid(self, request):
        if 'X-Authenticated-User' in request.headers:
            return AuthenticatedUser()


@implementer(IAuthorizationPolicy)
class AuthorizationPolicy(object):
    pass


def get_app():
    config = Configurator()
    config.add_route('hello', '/')
    config.add_view(hello_world, route_name='hello')
    config.scan('..request_log')
    config.set_authentication_policy(AuthenticationPolicy())
    config.set_authorization_policy(AuthorizationPolicy())
    request_log.authenticated_id = 'username'
    return TestApp(config.make_wsgi_app())
