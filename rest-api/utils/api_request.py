import json
from odoo.http import request


class ApiRequest:

    @staticmethod
    def get_json():
        if hasattr(request, "jsonrequest"):
            return request.jsonrequest or {}
        try:
            return json.loads(request.httprequest.data.decode('utf-8'))
        except Exception:
            return {}

    @staticmethod
    def get_query(kwargs, key, default=None, cast=None):
        value = kwargs.get(key, default)
        try:
            return cast(value) if cast else value
        except Exception:
            return default