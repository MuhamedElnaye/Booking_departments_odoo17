from odoo import models
#Three Types of model
class ModelCC(models.TransientModel):
    _name = "model.cc"


class ModelDD(models.AbstractModel):
    _name = 'model.dd'

class ModelEE(models.Model):
    _name = "model.ee"
    _log_access=False