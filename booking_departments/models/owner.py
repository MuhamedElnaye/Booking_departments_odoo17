from odoo import models,fields


class Owner(models.Model):
    _name = "owner"
    # _log_access=False

    name=fields.Char(required=True)
    phone=fields.Char()
    address=fields.Char()
    property_ids=fields.One2many("property","owner_id")