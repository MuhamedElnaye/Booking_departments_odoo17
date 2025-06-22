from odoo import models,fields,api

class Building(models.Model):
    _name = "building"
    _description = "Building view" # that show in chatter during create new property
    _inherit = ['mail.thread','mail.activity.mixin']
    # _rec_name = "code"
    # the record name(display name) that Under "Modul name" in app
    #Note:if this (_rec_name) Not found the "display name" link automatically with 'name' field if Found
    #  and '_rec_name' not Known

    no=fields.Integer()
    code=fields.Char()
    description=fields.Text()
    name=fields.Char()
    active=fields.Boolean(default=True)