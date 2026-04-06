# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json
from ..swagger.swagger_registry import swagger_registry


class SwaggerController(http.Controller):

    @http.route('/swagger', auth='public', type='http', website=True)
    def swagger_ui_page(self, **kwargs):
        return request.render('rest-api.swagger_ui')

    @http.route('/swagger.json', auth='public', type='http')
    def swagger_json(self, **kwargs):

        paths = {}
        tags = set()

        for ep in swagger_registry:
            path = ep["path"]
            method = ep["method"].lower()

            if path not in paths:
                paths[path] = {}

            # BASE STRUCTURE
            paths[path][method] = {
                "summary": ep.get("summary", ""),
                "tags": [ep.get("tag", "General")],
                "responses": {
                    "200": {"description": "Success"},
                    "400": {"description": "Bad Request"},
                    "401": {"description": "Unauthorized"},
                    "500": {"description": "Internal Server Error"},
                }
            }

            if ep.get("request_body"):
                paths[path][method]["requestBody"] = {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": ep["request_body"]
                        }
                    }
                }
            if ep.get("parameters"):
                paths[path][method]["parameters"] = ep["parameters"]

            if ep.get("auth"):
                paths[path][method]["security"] = [
                    {"BearerAuth": []}
                ]

            tags.add(ep.get("tag", "General"))

        swagger_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Smart REST API for Odoo",
                "description": "Official API documentation for Smart REST API module.",
                "version": "1.0.0"
            },
            "paths": paths,
            "tags": [{"name": t} for t in tags],
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    }
                }
            },
            "security": [{"BearerAuth": []}]
        }

        return request.make_response(
            json.dumps(swagger_spec),
            headers=[('Content-Type', 'application/json')]
        )