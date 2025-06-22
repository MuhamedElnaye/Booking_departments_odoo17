from odoo import models,fields


class SaleOrder(models.Model):
    _inherit = "sale.order" #sale.order coming with URL For Form or Tree View
    property_id=fields.Many2one('property')

    def action_confirm(self):
        res=super(SaleOrder,self).action_confirm()
        print("Inside action_confirm Method")
        return res
