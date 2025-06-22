from odoo import models,fields


class Client(models.Model):
    _name = "client"
    _log_access=False
    _inherit = 'owner'
