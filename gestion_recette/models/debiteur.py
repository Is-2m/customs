from odoo import models, fields

class Debiteur(models.Model):
    _name = 'or.debiteur'

    name = fields.Char()
    address = fields.Char()