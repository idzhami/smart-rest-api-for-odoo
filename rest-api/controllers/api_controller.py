# -*- coding: utf-8 -*-
import json
import jwt
from datetime import datetime, timedelta
from odoo import http
from odoo.http import request

from ..swagger.swagger_decorator import register_endpoint
from ..utils.api_request import ApiRequest
from ..utils.api_response import ApiResponse

SECRET_KEY = "TheKingkong__213424"


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')  # format for datetime
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')  # format for date
        elif isinstance(obj, bytes):
            return obj.decode('utf-8')  # decode bytes to string
        return super(CustomJSONEncoder, self).default(obj)


class ApiController(http.Controller):

    def parse_month(self, month_input):
        try:
            # Try to parse as a numeric month first
            return datetime.strptime(month_input, '%m').strftime('%B')
        except ValueError:
            # If that fails, try to parse as a full month name
            return datetime.strptime(month_input, '%B').strftime('%B')

    def _generate_jwt_token(self, user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=24),
            'iat': datetime.utcnow(),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return token

    def _authenticate_user(self, login, password):
        try:
            credential = {'login': login, 'password': password, 'type': 'password'}
            request.session.authenticate(request.db, credential)
            user = request.env.user
            return user
        except Exception:
            return None

    def _validate_token(self):
        auth_header = request.httprequest.headers.get('Authorization')

        if not auth_header:
            return {'message': "Token is required", "code": 401}, None

        try:
            # 🔥 SUPPORT Bearer
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
            else:
                token = auth_header

            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')

            user = request.env['res.users'].sudo().browse(user_id)
            if not user.exists():
                return {'message': "User not found", "code": 404}, None

        except jwt.ExpiredSignatureError:
            return {'message': "Token expired", "code": 401}, None

        except jwt.InvalidTokenError:
            return {'message': "Invalid token", "code": 401}, None

        return None, user

    # ================= LOGIN =================
    @http.route('/api/v1/login', type='json', auth='public', methods=['POST'], csrf=False)
    @register_endpoint(
        path="/api/v1/login",
        method="POST",
        summary="Login to get JWT Token",
        tag="Auth",
        auth=False,
        request_body={
            "type": "object",
            "properties": {
                "login": {"type": "string", "example": "admin"},
                "password": {"type": "string", "example": "admin"}
            },
            "required": ["login", "password"]
        }
    )
    def login(self, **kwargs):

        data = ApiRequest.get_json()

        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return ApiResponse.error("Missing login or password")

        user = self._authenticate_user(login, password)

        if not user:
            return ApiResponse.error("Invalid user or password")

        token = self._generate_jwt_token(user.id)

        user.sudo().write({'jwt_token': token})

        return ApiResponse.success({
            'token': token,
            'user': {
                'id': user.id,
                'login': user.login,
                'email': user.email,
            }
        })

    @register_endpoint(
        path="/api/v1/products",
        method="GET",
        summary="Get all products with pagination & filters",
        tag="Product",
        auth=True,
        parameters=[
            {"name": "page", "in": "query", "schema": {"type": "integer", "example": 1}},
            {"name": "size", "in": "query", "schema": {"type": "integer", "example": 10}},
            {"name": "name", "in": "query", "schema": {"type": "string"}},
            {"name": "category", "in": "query", "schema": {"type": "string"}}
        ]
    )
    @http.route('/api/v1/products', type='http', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):

        # 🔐 VALIDATE TOKEN
        error, user = self._validate_token()
        if error:
            return request.make_response(
                json.dumps(error),
                headers=[('Content-Type', 'application/json')],
                status=error.get("code", 401)
            )

        try:
            # ✅ PARAMS
            page = ApiRequest.get_query(kwargs, 'page', 1, int)
            size = ApiRequest.get_query(kwargs, 'size', 10, int)
            name = ApiRequest.get_query(kwargs, 'name')
            category = ApiRequest.get_query(kwargs, 'category')

            offset = (page - 1) * size

            # ✅ DOMAIN
            domain = []
            if name:
                domain.append(('name', 'ilike', name))

            if category:
                if str(category).isdigit():
                    domain.append(('categ_id', '=', int(category)))
                else:
                    domain.append(('categ_id.name', 'ilike', category))

            product_obj = request.env['product.template'].sudo()

            total = product_obj.search_count(domain)
            products = product_obj.search(domain, limit=size, offset=offset)

            data = [{
                'id': p.id,
                'name': p.name,
                'price': p.list_price,
                'qty': p.qty_available,
                'category': p.categ_id.name
            } for p in products]

            meta = {
                "page": page,
                "size": size,
                "total": total,
                "total_pages": (total + size - 1) // size
            }

            return request.make_response(
                json.dumps(ApiResponse.success(data, meta=meta), cls=CustomJSONEncoder),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps(ApiResponse.error(str(e), 500)),
                headers=[('Content-Type', 'application/json')],
                status=500
            )

    @register_endpoint(
        path="/api/v1/products",
        method="POST",
        summary="Create new product",
        tag="Product",
        auth=True,
        request_body={
            "type": "object",
            "properties": {
                "name": {"type": "string", "example": "Meja Kayu"},
                "default_code": {"type": "string", "example": "PRD001"},
                "list_price": {"type": "number", "example": 150000},
                "category_id": {"type": "integer", "example": 1},
                "uom_id": {"type": "integer", "example": 1}
            },
            "required": ["name"]
        }
    )
    @http.route('/api/v1/products', type='json', auth='public', methods=['POST'], csrf=False)
    def create_product(self, **kwargs):

        # 🔐 VALIDASI TOKEN
        error, user = self._validate_token()
        if error:
            return ApiResponse.error(error.get("message"), error.get("code"))

        try:
            data = ApiRequest.get_json()

            name = data.get('name')
            default_code = data.get('default_code')
            list_price = data.get('list_price', 0)
            category_id = data.get('category_id')
            uom_id = data.get('uom_id')

            # ❗ VALIDASI WAJIB
            if not name:
                return ApiResponse.error("Product name is required")

            # ✅ VALIDASI CATEGORY
            categ = None
            if category_id:
                categ = request.env['product.category'].sudo().browse(category_id)
                if not categ.exists():
                    return ApiResponse.error("Invalid category_id")

            # ✅ VALIDASI UOM
            uom = None
            if uom_id:
                uom = request.env['uom.uom'].sudo().browse(uom_id)
                if not uom.exists():
                    return ApiResponse.error("Invalid uom_id")

            # ✅ CREATE PRODUCT
            product = request.env['product.template'].sudo().create({
                'name': name,
                'default_code': default_code,
                'list_price': list_price,
                'categ_id': categ.id if categ else False,
                'uom_id': uom.id if uom else False,
                'uom_po_id': uom.id if uom else False,
            })

            # ✅ RESPONSE
            return ApiResponse.success({
                "id": product.id,
                "name": product.name,
                "default_code": product.default_code,
                "price": product.list_price,
                "category": product.categ_id.name if product.categ_id else None
            }, message="Product created successfully")

        except Exception as e:
            return ApiResponse.error(str(e), 500)

    @register_endpoint(
        path="/api/v1/products/{product_id}",
        method="PUT",
        summary="Update product",
        tag="Product",
        auth=True,
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "example": 10
            }
        ],
        request_body={
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "list_price": {"type": "number"}
            }
        }
    )
    @http.route('/api/v1/products/<int:product_id>', type='json', auth='public', methods=['PUT'], csrf=False)
    def update_product(self, product_id, **kwargs):

        # 🔐 VALIDASI TOKEN
        error, user = self._validate_token()
        if error:
            return ApiResponse.error(error.get("message"), error.get("code"))

        try:
            product = request.env['product.template'].sudo().browse(product_id)

            if not product.exists():
                return ApiResponse.error("Product not found", 404)

            data = ApiRequest.get_json()

            vals = {}

            # ✅ FIELD UPDATE (flexible)
            if 'name' in data:
                vals['name'] = data.get('name')

            if 'default_code' in data:
                vals['default_code'] = data.get('default_code')

            if 'list_price' in data:
                vals['list_price'] = data.get('list_price')

            if 'category_id' in data:
                categ = request.env['product.category'].sudo().browse(data.get('category_id'))
                if not categ.exists():
                    return ApiResponse.error("Invalid category_id")
                vals['categ_id'] = categ.id

            if 'uom_id' in data:
                uom = request.env['uom.uom'].sudo().browse(data.get('uom_id'))
                if not uom.exists():
                    return ApiResponse.error("Invalid uom_id")
                vals['uom_id'] = uom.id
                vals['uom_po_id'] = uom.id

            # ❗ CEK DUPLICATE DEFAULT CODE
            if 'default_code' in vals:
                existing = request.env['product.template'].sudo().search([
                    ('default_code', '=', vals['default_code']),
                    ('id', '!=', product.id)
                ], limit=1)

                if existing:
                    return ApiResponse.error("Product code already exists")

            # ✅ UPDATE
            product.write(vals)

            return ApiResponse.success({
                "id": product.id,
                "name": product.name,
                "default_code": product.default_code,
                "price": product.list_price
            }, message="Product updated successfully")

        except Exception as e:
            return ApiResponse.error(str(e), 500)


    @register_endpoint(
        path="/api/v1/products/{product_id}",
        method="DELETE",
        summary="Delete product",
        tag="Product",
        auth=True,
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "example": 10
            }
        ]
    )
    @http.route('/api/v1/products/<int:product_id>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def delete_product(self, product_id, **kwargs):

        # 🔐 VALIDASI TOKEN
        error, user = self._validate_token()
        if error:
            return request.make_response(
                json.dumps(ApiResponse.error(error.get("message"), error.get("code"))),
                headers=[('Content-Type', 'application/json')],
                status=error.get("code", 401)
            )

        try:
            product = request.env['product.template'].sudo().browse(product_id)

            if not product.exists():
                return request.make_response(
                    json.dumps(ApiResponse.error("Product not found", 404)),
                    headers=[('Content-Type', 'application/json')],
                    status=404
                )

            product.unlink()

            return request.make_response(
                json.dumps(ApiResponse.success(message="Product deleted successfully")),
                headers=[('Content-Type', 'application/json')]
            )

        except Exception as e:
            return request.make_response(
                json.dumps(ApiResponse.error(str(e), 500)),
                headers=[('Content-Type', 'application/json')],
                status=500
            )
