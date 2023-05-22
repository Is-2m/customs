from odoo import models, fields

class Debiteur(models.Model):
    _name = 'finance.debiteur'

    name = fields.Char()
    address = fields.Char()