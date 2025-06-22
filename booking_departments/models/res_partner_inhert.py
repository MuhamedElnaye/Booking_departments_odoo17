from odoo import models,fields,api


class ResPartner(models.Model):
    _inherit = "res.partner" #sale.order coming with URL For Form or Tree View
    property_id=fields.Many2one('property') #"property" model name in "property.py" file
    #There are Two Methods For Doing Compute Or relations
    # [1]
    price=fields.Float(related="property_id.selling_price")

    #[2]
    # price=fields.Float(compute="_compute_price")
    # @api.depends("property_id")  #we are using this to can change price automatically during chang properties
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price=rec.property_id.selling_price