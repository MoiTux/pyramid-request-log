# pyramid-request-log

A pyramid plugin that will log all Request and Response.  
If a json body is available it will also be logged, a list of
forbidden key can be used to not logged sensitive information.

## Configuration

`pyramid_request_log.request_log` a list a key pattern to to log,
it will be replace with '******'

`pyramid_request_log.authenticated_id` if you have create your own
authentication mechanism, you can set the property you want to help
'identity' who did the request

## Example

```
$ curl -H "X-User: xxxx" 127.0.0.1:6543/something?test=ok
INFO  [pyramid_request_log.request_log] New request: GET /something?test=ok (user: MoiTux)
INFO  [pyramid_request_log.request_log] Response for request: GET /something?test=ok: HTTPCode: 200 OK, (body: {'value': 42}) (user: MoiTux)
```

## Code status

[![Build Status](https://travis-ci.org/MoiTux/pyramid-request-log.svg?branch=master)](https://travis-ci.org/MoiTux/pyramid-request-log)
[![Coverage Status](https://coveralls.io/repos/github/MoiTux/pyramid-request-log/badge.svg?branch=master)](https://coveralls.io/github/MoiTux/pyramid-request-log?branch=master)