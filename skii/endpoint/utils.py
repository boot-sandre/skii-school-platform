from devtools import debug
from django.http import HttpRequest
from ninja import Schema


def devtools_debug(func):
    def wrapper(request: HttpRequest, payload: Schema):
        debug(request, payload)
        response = func(request, payload=payload)
        debug(response)
        return response

    return wrapper
