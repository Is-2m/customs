from odoo import models, fields

class Ordonnateur(models.Model):
    _name = 'or.ordonnateur'

    name = fields.Char()

    comptes = fields.One2many(
        'or.compte',
        'ordonnateur_id',
        string='Comptes',
    )

    # Any other fields for Ordonnateur table

