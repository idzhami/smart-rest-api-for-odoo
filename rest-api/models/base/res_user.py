from odoo import models, fields
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError

class ResUsers(models.Model):
    _inherit = 'res.users'

    jwt_token = fields.Char(string="JWT Token")