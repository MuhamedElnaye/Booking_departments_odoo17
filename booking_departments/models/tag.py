from odoo import models,fields


class Tags(models.Model):
    _name = "tags"
    # _log_access=False

    name=fields.Char(required=True)
