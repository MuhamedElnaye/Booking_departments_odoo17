from odoo import models,fields


class AccountMove(models.Model):
    _inherit = "account.move" #sale.order coming with URL For Form or Tree View


    def action_do_somthing(self):
        print(self,'Inside action_do_somthing')
