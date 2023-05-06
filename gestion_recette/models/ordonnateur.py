from odoo import models, fields

class Ordonnateur(models.Model):
    _name = 'or.ordonnateur'

    name = fields.Char()
    # Any other fields for Ordonnateur table

