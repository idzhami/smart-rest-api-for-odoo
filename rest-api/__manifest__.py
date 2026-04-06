# -*- coding: utf-8 -*-
{
    'name': "Smart REST API for Odoo",
    'version': '18.0.1.0.0',
    'summary': "Powerful REST API framework for seamless Odoo integration with external systems.",

    'description': """
Smart REST API for Odoo
======================

A powerful and flexible REST API framework designed to simplify integration between Odoo and external applications such as mobile apps, web platforms, and third-party systems.

Key Features:
-------------
- Secure REST API endpoints (JWT Authentication ready)
- Easy integration with mobile & frontend applications
- Standardized JSON response structure
- Built-in Swagger UI for API documentation
- Custom endpoint support
- Scalable and developer-friendly architecture

Use Cases:
----------
- Mobile App Integration (Android / iOS)
- Third-party system integration
- Headless Odoo implementation
- Middleware / API Gateway

Why Choose This Module:
----------------------
This module is built for developers and companies who need a reliable, scalable, and clean API layer on top of Odoo without complex configuration.

Developed by Usman Idzhami.
    """,

    'category': 'Technical',
    'author': "Usman Idzhami",
    'website': "https://www.linkedin.com/in/usman-idzhami-a8a5021b9/",
    'maintainer': 'idzhami',

    'license': 'LGPL-3',

    'depends': [
        'base',
        'web',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/swagger_ui.xml',
    ],


    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}